# FILE_HOLDER_BY_DMITRIEV_SS


## What user can do

1. Upload file (/upload). File will added in DB with owner id. If file with this hash exist - nothing happen.

    ALLOWED_EXTENSIONS: txt, pdf, png, jpg, jpeg, gif, xlsx

    File will be saved in dir what named like two first letters of file hash.
    File will be saved with new name: "file_hash"."file_extension"
    For example if we want to save file example.txt and hash of that file is: "abc123"
    we will save that file by path "filestore/ab/abc123.txt"

2. Delete file (/delete). Nobody can delete it, but owner can.

3. Download file (/download). Everybody can download file.

## Auth

Auth required for /upload endpoint and /delete endpoint

For auth user can use /login. For logout - /logout
Registration not implemented

For test auth you can add your user in DB in table "user"
Login = user's login
Password = Your password Hashed by flask Bcrypt. 
You can hash your password by pw_hash = bcrypt.generate_password_hash('secret', 10)

## How to run app

1. Run PostgreSQL

2. Create .env file in root of project
    For example:

        UPLOAD_FOLDER="ABC\\PATH\\TO\\filestore"
        SECRET_KEY=b'SUPER_PUPER_SECRET'

        DB_USER=user_puzer
        DB_PASSWORD=secret
        DB_NAME=file_holder_db
        DB_HOST=localhost
        DB_PORT=5432T

3. Create env
   
    python -m venv venv

4. Source venv

    For win: venv\Scripys\activate

5. Install req
    pip install -r requirements.txt

6. Upgrade DB (apply migrations)

    alembic upgrade head

7. Run app
    
    flask --app src/application/app run
