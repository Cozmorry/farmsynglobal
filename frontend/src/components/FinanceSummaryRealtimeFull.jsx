// src/components/FinanceSummaryRealtimeFull.jsx
import React, { useEffect, useState, useRef } from "react";
import api from "../api";

const FinanceSummaryRealtimeFull = ({ farmId, moduleType, entityId = null }) => {
  const [entries, setEntries] = useState([]);
  const [totals, setTotals] = useState({ totalIncome: 0, totalExpense: 0, netProfit: 0 });
  const wsRef = useRef(null);

  // -----------------------------
  // Helper to calculate totals
  // -----------------------------
  const recalcTotals = (entries) => {
    const totalIncome = entries.filter(e => e.category === "income").reduce((sum, e) => sum + e.amount, 0);
    const totalExpense = entries.filter(e => e.category === "expense").reduce((sum, e) => sum + e.amount, 0);
    setTotals({ totalIncome, totalExpense, netProfit: totalIncome - totalExpense });
  };

  // -----------------------------
  // Fetch entries
  // -----------------------------
  const fetchEntries = async () => {
    try {
      const params = { farm_id: farmId, module_type: moduleType };
      if (entityId) params.entity_id = entityId;
      const res = await api.get("/finance/module_summary", { params });
      setEntries(res.data.entries);
      recalcTotals(res.data.entries);
    } catch (err) {
      console.error("Failed to fetch finance entries", err);
    }
  };

  // -----------------------------
  // Add entry (optimistic)
  // -----------------------------
  const addEntry = async (entry) => {
    const tempId = "temp-" + Date.now();
    const optimisticEntry = { ...entry, id: tempId };
    setEntries(prev => [...prev, optimisticEntry]);
    recalcTotals([...entries, optimisticEntry]);

    try {
      const res = await api.post("/finance/module_entry", { ...entry, module_type: moduleType });
      setEntries(prev => prev.map(e => (e.id === tempId ? res.data : e)));
      recalcTotals([...entries.filter(e => e.id !== tempId), res.data]);
    } catch (err) {
      setEntries(prev => prev.filter(e => e.id !== tempId));
      recalcTotals(entries.filter(e => e.id !== tempId));
      alert("Failed to add entry.");
    }
  };

  // -----------------------------
  // Update entry
  // -----------------------------
  const updateEntry = async (id, updatedFields) => {
    setEntries(prev => prev.map(e => (e.id === id ? { ...e, ...updatedFields } : e)));
    recalcTotals(entries.map(e => (e.id === id ? { ...e, ...updatedFields } : e)));

    try {
      await api.put(`/finance/module_entry/${id}`, { ...updatedFields, module_type: moduleType });
      fetchEntries(); // confirm backend state
    } catch (err) {
      console.error("Failed to update entry", err);
      fetchEntries(); // revert if failed
    }
  };

  // -----------------------------
  // Delete entry
  // -----------------------------
  const deleteEntry = async (id) => {
    setEntries(prev => prev.filter(e => e.id !== id));
    recalcTotals(entries.filter(e => e.id !== id));

    try {
      await api.delete(`/finance/module_entry/${id}`, { data: { module_type: moduleType } });
    } catch (err) {
      console.error("Failed to delete entry", err);
      fetchEntries(); // revert if failed
    }
  };

  // -----------------------------
  // Drag-and-drop (simple)
  // -----------------------------
  const moveEntry = (fromIdx, toIdx) => {
    const updated = [...entries];
    const [moved] = updated.splice(fromIdx, 1);
    updated.splice(toIdx, 0, moved);
    setEntries(updated);
  };

  // -----------------------------
  // WebSocket
  // -----------------------------
  useEffect(() => {
    fetchEntries();

    wsRef.current = new WebSocket(`ws://localhost:8000/ws/finance/${farmId}`);
    wsRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.event === "finance_updated") {
        fetchEntries();
      }
    };

    return () => wsRef.current.close();
  }, [farmId, moduleType, entityId]);

  return (
    <div>
      <h3>{moduleType.charAt(0).toUpperCase() + moduleType.slice(1)} Finance Summary</h3>
      <p>Total Income: {totals.totalIncome.toFixed(2)}</p>
      <p>Total Expense: {totals.totalExpense.toFixed(2)}</p>
      <p>Net Profit: {totals.netProfit.toFixed(2)}</p>

      <button onClick={() => addEntry({ description: "New Entry", amount: 0, category: "expense" })}>
        Add Entry
      </button>

      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Description</th>
            <th>Category</th>
            <th>Amount</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {entries.map((e, idx) => (
            <tr key={e.id}>
              <td>{idx + 1}</td>
              <td>
                <input
                  type="text"
                  value={e.description}
                  onChange={(ev) => updateEntry(e.id, { description: ev.target.value })}
                />
              </td>
              <td>{e.category}</td>
              <td>
                <input
                  type="number"
                  value={e.amount}
                  onChange={(ev) => updateEntry(e.id, { amount: parseFloat(ev.target.value) || 0 })}
                />
              </td>
              <td>
                <button onClick={() => deleteEntry(e.id)}>Delete</button>
                {idx > 0 && <button onClick={() => moveEntry(idx, idx - 1)}>↑</button>}
                {idx < entries.length - 1 && <button onClick={() => moveEntry(idx, idx + 1)}>↓</button>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FinanceSummaryRealtimeFull;

















# backend/finance_ws.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust to your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# WebSocket manager
# -----------------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}  # farm_id -> list of sockets

    async def connect(self, farm_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(farm_id, []).append(websocket)

    def disconnect(self, farm_id: int, websocket: WebSocket):
        self.active_connections[farm_id].remove(websocket)
        if not self.active_connections[farm_id]:
            del self.active_connections[farm_id]

    async def broadcast(self, farm_id: int, message: dict):
        if farm_id in self.active_connections:
            for connection in self.active_connections[farm_id]:
                await connection.send_json(message)


manager = ConnectionManager()

# -----------------------------
# WebSocket endpoint
# -----------------------------
@app.websocket("/ws/finance/{farm_id}")
async def finance_ws(farm_id: int, websocket: WebSocket):
    await manager.connect(farm_id, websocket)
    try:
        while True:
            # Just keep the connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(farm_id, websocket)


# -----------------------------
# Broadcast helper (call after DB changes)
# -----------------------------
async def notify_finance_update(farm_id: int):
    await manager.broadcast(farm_id, {"event": "finance_updated"})
