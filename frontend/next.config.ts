import path from 'path';
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  outputFileTracingRoot: path.join(__dirname),
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
