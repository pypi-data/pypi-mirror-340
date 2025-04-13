# pyqueuex 🚀

A powerful, feature-rich job queue system for Python with advanced retry strategies, job chaining, and intelligent job processing.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Redis](https://img.shields.io/badge/Redis-Required-red.svg)](https://redis.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI Version](https://img.shields.io/pypi/v/pyqueuex)](https://pypi.org/project/pyqueuex/)

## ✨ Features

- 🔄 **Advanced Retry Strategies**
  - Exponential, Linear, and Fixed backoff
  - Configurable delays and attempts
  - Maximum retry limit

- ⏱️ **Smart Job Processing**
  - Job timeout handling
  - Time-to-live (TTL) support
  - Multiple queue processing strategies
  - Concurrent job execution

- 🔗 **Job Dependencies & Chaining**
  - Sequential job execution
  - Result passing between jobs
  - Complex workflow support
  - Dependency graph management

- 📊 **Queue Management**
  - FIFO/LIFO processing
  - Priority queues
  - Round-robin distribution
  - Rate limiting

## 🚀 Quick Start

```bash
pip install pyqueuex