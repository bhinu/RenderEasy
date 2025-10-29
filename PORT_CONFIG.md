# Port Configuration

## Current Ports

- **Backend:** Port **5001** (changed from 5000)
- **Frontend:** Port **3000**

## Why Port 5001?

On macOS, port 5000 is often used by **AirPlay Receiver** service, which causes conflicts with Flask.

### Solution Applied

The backend has been configured to use port **5001** instead.

## Accessing the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5001/api
- **Health Check:** http://localhost:5001/api/health

## If You Need to Change Ports

### Change Backend Port

Edit `backend/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5001 to your port
```

Then update `frontend/.env`:
```
REACT_APP_API_URL=http://localhost:YOUR_PORT/api
```

### Change Frontend Port

Set environment variable before starting:
```bash
PORT=3001 npm start
```

Or create `frontend/.env.local`:
```
PORT=3001
```

## Disabling AirPlay Receiver (Alternative)

If you prefer to use port 5000:

1. Open **System Settings** (macOS 13+) or **System Preferences** (older macOS)
2. Go to **General** → **AirDrop & Handoff**
3. Disable **AirPlay Receiver**

Then change backend port back to 5000:
- Edit `backend/app.py` (line 489)
- Edit `frontend/.env`

## Testing Connection

```bash
# Test backend
curl http://localhost:5001/api/health

# Expected response:
# {"status":"healthy","message":"RenderEase API is running"}
```

## Common Port Issues

### "Address already in use"

Find what's using the port:
```bash
lsof -i :5001
```

Kill the process:
```bash
kill -9 <PID>
```

### CORS Errors

Make sure `frontend/.env` matches backend port:
```bash
cat frontend/.env
# Should show: REACT_APP_API_URL=http://localhost:5001/api
```

If you changed it, restart the frontend:
```bash
cd frontend
npm start
```
