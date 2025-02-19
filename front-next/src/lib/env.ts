const requiredEnvVars = [
    'DB_USER',
    'DB_PASSWORD',
    'DB_NAME',
    'DB_HOST',
    'DB_PORT',
    'CRAWLER_URL',
    'JWT_SECRET',
];
const missingVars = requiredEnvVars.filter((key) => !process.env[key]);

if (missingVars.length > 0) {
    console.error(`Missing environment variables: ${missingVars.join(', ')}`);
    throw new Error('Database configuration error');
}

export const DB_USER = process.env.DB_USER!;
export const DB_PASSWORD = process.env.DB_PASSWORD!;
export const DB_NAME = process.env.DB_NAME!;
export const DB_HOST = process.env.DB_HOST!;
export const DB_PORT = process.env.DB_PORT!;
export const CRAWLER_URL = process.env.CRAWLER_URL!;
export const JWT_SECRET = process.env.JWT_SECRET!;
