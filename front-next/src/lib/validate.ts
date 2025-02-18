import { z } from 'zod';

const noSpecialChars = /^[0-9a-zA-Z_.-]+$/;

export const userSchema = z.object({
    username: z
        .string()
        .min(3, 'Username must be at least 3 characters long')
        .max(30, 'Username too long')
        .regex(noSpecialChars, 'Invalid characters in username'),
    password: z
        .string()
        .min(6, 'Password must be at least 6 characters long')
        .max(30, 'Password too long')
        .regex(noSpecialChars, 'Invalid characters in username'),
});
