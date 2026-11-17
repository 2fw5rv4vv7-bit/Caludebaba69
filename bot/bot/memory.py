
import asyncpg


class Memory:
    def __init__(self, database_url):
        self.database_url = database_url
        self.pool = None

    async def connect(self):
        if not self.database_url:
            raise RuntimeError("DATABASE_URL is missing")

        url = self.database_url.replace(
            "postgres://",
            "postgresql://",
            1
        )

        self.pool = await asyncpg.create_pool(
            url,
            min_size=1,
            max_size=5
        )

        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id BIGSERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMPTZ
                        DEFAULT NOW()
                )
            """)

    async def add(self, user_id, role, content):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO messages
                (user_id, role, content)
                VALUES ($1, $2, $3)
                """,
                user_id,
                role,
                content
            )

    async def get_history(self, user_id, limit=20):
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT role, content
                FROM (
                    SELECT id, role, content
                    FROM messages
                    WHERE user_id = $1
                    ORDER BY id DESC
                    LIMIT $2
                ) recent
                ORDER BY id ASC
                """,
                user_id,
                limit
            )

        return [
            {
                "role": row["role"],
                "content": row["content"]
            }
            for row in rows
        ]

    async def reset(self, user_id):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM messages WHERE user_id = $1",
                user_id
            )

    async def close(self):
        if self.pool:
            await self.pool.close()
