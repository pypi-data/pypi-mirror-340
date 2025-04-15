# 25.1

- Add Python 3.13, remove Python 3.8 support.

# 24.4

- Better error message for 4xx HTTP codes (e.g. expired access token)

# 24.3

- Return the plain `requests` response if it is not a JSON content.
  This allows to download attachments, for example.

# 24.2

- Fix bug: work items cannot be created due to wrong content-type (Now use json 
  patch content type if the payload is an array, not just for PATCH HTTP method)

# 24.1

- Add `call` method to have unified simple interface for all API endpoints

# 23.6

- Retry on proxy error

# 23.5

- Fix Content-Type header

# 23.4

- Fix: remove forgotten print function
- Add detailed example

# 23.3

- Add `api` method, so API endpoints can be copy-pasted from Azure DevOps documentation.

# 23.2

- Internal change: use pyproject.toml instead of setup.py

# 22.12.0

- Initial version
