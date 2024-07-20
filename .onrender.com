databases:
  - name: image_galleryr
    plan: free
    databaseName: anime_wallpaper
    user: anime_wallpaper_user

services:
  - type: web
    plan: free
    name: mysite
    runtime: python
    buildCommand: "./build.sh"
    startCommand: "python -m gunicorn mysite.asgi:application -k uvicorn.workers.UvicornWorker"
    envVars:
      - key: postgresql://anime_wallpaper_user:1XoYqHm6KX912QFZJdGdCWtCa1vffjwx@dpg-cqdl7c0gph6c73a87a40-a/anime_wallpaper
        fromDatabase:
          name: anime_wallpaper
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: WEB_CONCURRENCY
        value: 4
