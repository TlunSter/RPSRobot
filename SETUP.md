# RPSRobot Setup

## 1. Install Git

Install Git for Windows.

## 2. Install uv

Run in PowerShell:

powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

Restart PowerShell afterward.

## 3. Clone the repository

git clone https://github.com/TlunSter/RPSRobot.git

cd RPSRobot

## 4. Set up the Python project

cd Python\RPSRobot

uv sync

## 5. Run the Python program

uv run python main.py

## 6. PlatformIO

Open:

PlatformIO\ESP32ArmController

in VS Code with the PlatformIO extension installed.

## Updating the project later

From the repository root:

git pull

For Python dependencies:

cd Python\RPSRobot
uv sync