<div align="center">
<img src="./img/logo_main.png" alt="PyDOGE Logo" width= "176">
<p>A Python library to interact with Department of Government Efficiency (DOGE) API.</p>
</div>

<br>

<details open="true">
  <summary><strong> 🧾 Table of Contents</strong></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#highlights">Highlights</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a>
      <ul>
        <li><a href="#synchronous-fetching">Synchronous Fetching</a></li>
        <li><a href="#asynchronous-pagination">Asynchronous Pagination</a></li>
      </ul>
    </li>
    <li><a href="#contributors">Contributors </a></li>
    <li><a href="#acknowledgments">Acknowledgements </a></li>
  </ol>
</details>

## 🐍 About The Project
PyDOGE API is an advanced, Python wrapper for interacting with the public-facing API of the **Department of Government Efficiency (DOGE)** — a federal initiative aimed at increasing transparency and fiscal accountability by sharing detailed datasets on:

- 💸 Cancelled grants
- 📑 Contract terminations
- 🏢 Lease reductions
- 🧾 Payment transactions

## 🚀 Features

- Auto-pagination (sync or async, fetch all pages if needed)
- `.export()` to CSV, Excel, or JSON with timestamped filenames  
- `.to_dataframe()` for Pandas users 
- `.summary()` with analytics (rows, nulls, dtypes, stats)  
- `summary(save_as="...")` for file logging  
- Returns Pydantic models & dict output
- Retry-safe client with 429 handling

This package enables data scientists and analysts to **programmatically access and analyze** the data with ease.

<!--Getting Started-->
## 📌 Getting Started

### Installation

Install:
```bash
pip install pydoge-api
```
Upgrade:
```
pip install --upgrade pydoge-api
```

**Documentation**

Full developer docs with API reference, usage, and model schema:

- 👉 [Docs and Examples (PyDOGE)](https://ihassan8.github.io/pydoge-api/)
- 👉 [Official Swagger Page](https://api.doge.gov/docs)

## 📚 Usage

### Synchronous Fetching

```python
from pydoge_api import DogeAPI

api = DogeAPI(
    fetch_all=True,             # get all pages
    output_pydantic=False,      # dict output
    handle_response=True,       # parse response
    run_async=False             # ← synchronous mode
)

# Grants sorted by savings
grants = api.savings.get_grants(sort_by="savings")

# Filter payments by agency
payments = api.payments.get_payments(filter="agency", filter_value="NASA")

```

### Asynchronous Pagination

```python
api = DogeAPI(
    fetch_all=True,
    output_pydantic=True,
    handle_response=True,
    run_async=True              # ← enable async parallel fetch
)

grants = api.savings.get_grants(sort_by="value")
print(grants.meta.total_results)
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 👪 Contributors
All contributions are welcome. If you have a suggestion that would make this better, please fork the repo and create a merge request. You can also simply open an issue with the label 'enhancement'.

Don't forget to give the project a star! Thanks again!


## 👏 Acknowledgments
Inspiration, code snippets, etc.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
