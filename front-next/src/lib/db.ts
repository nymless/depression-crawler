import { Pool } from 'pg';
import { DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER } from './env';

export interface User {
    id: number;
    username: string;
    password: string;
}

const pool = new Pool({
    user: DB_USER,
    host: DB_HOST,
    database: DB_NAME,
    password: DB_PASSWORD,
    port: Number(DB_PORT),
});

export async function openDB() {
    return pool;
}

async function initDB() {
    await pool.query(`
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    `);
}

let dbInitialized = false;

if (!dbInitialized) {
    try {
        await initDB();
        dbInitialized = true;
        console.log('Database initialized successfully!');
    } catch (error) {
        console.error('Database initialization failed:', error);
    }
}
