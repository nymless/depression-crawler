import { Pool } from "pg";

export interface User {
    id: number;
    username: string;
    password: string;
}

const requiredEnvVars = [
    "DB_USER",
    "DB_PASSWORD",
    "DB_NAME",
    "DB_HOST",
    "DB_PORT",
];
const missingVars = requiredEnvVars.filter((key) => !process.env[key]);

if (missingVars.length > 0) {
    console.error(`Missing environment variables: ${missingVars.join(", ")}`);
    throw new Error("Database configuration error");
}

const pool = new Pool({
    user: process.env.DB_USER,
    host: process.env.DB_HOST,
    database: process.env.DB_NAME,
    password: process.env.DB_PASSWORD,
    port: Number(process.env.DB_PORT),
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
        console.log("Database initialized successfully!");
    } catch (error) {
        console.error("Database initialization failed:", error);
    }
}
