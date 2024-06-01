const variables = {
  NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
} as const;

type Variables = typeof variables;

export const env = (key: keyof Variables) => {
  return process.env[key];
};
