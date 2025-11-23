# CS2 Online Dumper

Automated system for extracting, storing, and distributing Counter-Strike 2 offsets and schema data.

## Tech Stack

**Backend**
- Python 3.10+
- FastAPI
- SQLModel (SQLAlchemy)
- PostgreSQL

**Frontend**
- React 18
- Vite
- Tailwind CSS

**Worker (Local)**
- Python
- `cs2-dumper.exe` (External Dependency)

**Infrastructure**
- Docker & Docker Compose

## Architecture

1. **Local Worker**: Runs `cs2-dumper.exe`, hashes output files, and uploads changes to the API.
2. **API**: Validates authentication (`x-api-key`), stores JSON data in PostgreSQL, and serves the latest versions.
3. **Front**: Fetches and displays the latest offsets with search and download capabilities.

## Credits

- **CS2 Dumper**: [a2x/cs2-dumper](https://github.com/a2x/cs2-dumper) - The core executable used for extracting offsets.
