# stock-flow

A simple command-line inventory management system built in Python.
StockFlow allows users to manage product stock with basic inventory operations such as product registration, stock entry, and stock withdrawal, while keeping a persistent record using JSON files.

Features
- Add new products to inventory
Update existing product quantities
Withdraw products with stock validation
Automatic stock updates
Transaction logging (entries and withdrawals)
Persistent data storage using JSON files
Simple command-line interface (CLI)
🧠 How it works

StockFlow simulates a basic warehouse system:

Products are stored with an ID, name, and quantity
Every change in stock is recorded as a transaction
Data is saved locally in JSON files:
produtos.json → product database
transacoes.json → transaction history
The system loads data automatically when started
🛠 Technologies Used
Python 3
JSON (data persistence)
Object-Oriented Programming (OOP)
CLI-based interaction
Standard library (json, os, datetime, pathlib)
