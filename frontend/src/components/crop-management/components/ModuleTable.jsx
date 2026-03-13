//src/components/crop_management/components/ModuleTable.jsx
import React from "react";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography } from "@mui/material";

/**
 * ModuleTable - reusable table for any entity
 *
 * Props:
 * - title: string - table title
 * - data: array of objects - API response
 * - actions: optional function returning action buttons per row
 */
const ModuleTable = ({ title, data = [], actions }) => {
  if (!Array.isArray(data) || data.length === 0) {
    return (
      <Paper sx={{ p: 2, my: 3 }}>
        <Typography variant="h6">{title}</Typography>
        <Typography>No data available</Typography>
      </Paper>
    );
  }

  const headers = Object.keys(data[0]);

  return (
    <TableContainer component={Paper} sx={{ my: 3 }}>
      <Typography variant="h6" sx={{ p: 2 }}>{title}</Typography>
      <Table>
        <TableHead>
          <TableRow>
            {headers.map((header) => (
              <TableCell key={header} sx={{ fontWeight: "bold" }}>
                {header.replace(/([A-Z])/g, " $1")}
              </TableCell>
            ))}
            {actions && <TableCell>Actions</TableCell>}
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((row, index) => (
            <TableRow key={index}>
              {headers.map((header) => (
                <TableCell key={header}>{row[header]?.toString() || "-"}</TableCell>
              ))}
              {actions && <TableCell>{actions(row)}</TableCell>}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default ModuleTable;
