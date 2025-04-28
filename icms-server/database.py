from datatypes import User
import aiosqlite
import bcrypt
import asyncio
import json
import jwt.api_jwt
import datetime


async def reset_database():
    async with aiosqlite.connect('database.db') as db:
        await db.execute("DROP TABLE users;")

        table = """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            token TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            devices TEXT NOT NULL,
            admin BOOLEAN NOT NULL,
            roles TEXT NOT NULL
        ); 
        """
        await db.execute(table)
        await db.commit()

async def db_create_database():
    async with aiosqlite.connect('database.db') as db:
        table = """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            token TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            devices TEXT NOT NULL,
            admin BOOLEAN NOT NULL,
            roles TEXT NOT NULL
        ); 
        """
        await db.execute(table)
        await db.commit()    

async def db_get_user_by_id(user_id: int) -> User:
    async with aiosqlite.connect('database.db') as db:
        query = "SELECT * FROM users WHERE id = ?"
        cursor = await db.execute(query, (user_id, ))
        row = await cursor.fetchone()
        user: User = await from_row(row)

        return user

async def db_get_user_by_username(username: str) -> User:
    async with aiosqlite.connect('database.db') as db:
        query = "SELECT * FROM users WHERE username = ?"
        cursor = await db.execute(query, (username, ))
        row = await cursor.fetchone()
        user: User = await from_row(row)

        return user
    
async def from_row(row: aiosqlite.Row) -> User:
    try:
        user: User = User(username=row[2], password=row[3], token=row[1], id=row[0])
        user.devices = json.loads(row[4])
        user.is_admin = row[5]
        user.roles = json.loads(row[6])
        return user
    except Exception as e:
        return None


async def db_get_users() -> list[User]:
    async with aiosqlite.connect('database.db') as db:
        users: list[User] = []

        query = "SELECT * FROM users"
        rows = await db.execute_fetchall(query)

        for row in rows:
            user: User = await from_row(row)

            if user is None:
                continue

            users.append(user)

        return users

async def generate_user_token(user_id: int) -> str:
    user_token = jwt.api_jwt.encode(
        {
            "user_id": user_id,
            "exp": datetime.datetime.now() + datetime.timedelta(days=30)
        },
        "secret",
        algorithm="HS256"
    )

    return user_token


async def db_create_user(user: User) -> User:
    async with aiosqlite.connect('database.db') as db:
        query = """
        INSERT INTO users (
            token,
            username,
            password,
            devices,
            admin,
            roles
        ) VALUES (?, ?, ?, ?, ?, ?);"""

        devices = json.dumps(user.devices)
        roles = json.dumps(user.roles)

        await db.execute(query, ('', user.username, user.password, devices, user.is_admin, roles))
        await db.commit()

        #this is a horrible hack to try and generate an id using the database       
        #select the user after adding it to the database with no token
        #this is literally only so it will generate an id for us 
        query = "SELECT * FROM users WHERE username = ?"
        cursor = await db.execute(query, (user.username, ))
        row = await cursor.fetchone()
        user: User = await from_row(row)

        #generate a token and then update the database row with the new user token
        token: str = await generate_user_token(user.id)
        query = "UPDATE users SET token = ? WHERE username = ?"
        await db.execute(query, (token, user.username))
        await db.commit()

        #make the current user token the generated token
        user.current_token = token
        return user

if __name__ == "__main__":
    #asyncio.run(reset_database())
    #asyncio.run(create_user(User("testusername", "testpassword", "testtoken")))
    #asyncio.run(get_user_by_username('testusername'))
    #asyncio.run(get_users())
    #asyncio.run(get_user_by_id(1))
    pass