/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
        return [
            {
                source: '/backend:8000*',
                destination: 'http://localhost:8000*',
            },
        ];
    },
};

export default nextConfig;
