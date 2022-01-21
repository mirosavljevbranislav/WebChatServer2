import uvicorn

if __name__ == '__main__':
    uvicorn.run('app.server.server:app', reload=True)
