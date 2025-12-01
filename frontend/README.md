# BlaBlaTrip Frontend

This is the Next.js frontend for the BlaBlaTrip application.

## Getting Started

### Using Docker (Recommended)

The easiest way to run the frontend is using Docker Compose from the root directory:

```bash
docker compose up --build
```

The frontend will be available at [http://localhost:3000](http://localhost:3000).

### Running Locally

If you have Node.js installed, you can run the frontend locally:

1. Install dependencies:
   ```bash
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000) with your browser.

## Project Structure

- `src/app`: App Router pages and layouts.
- `src/components`: Reusable UI components.
- `public`: Static assets.
