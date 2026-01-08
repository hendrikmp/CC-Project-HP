/** @type {import('next').NextConfig} */
const nextConfig = {
  // 1. Disable source maps to save memory
  productionBrowserSourceMaps: false,
  
  // 2. Reduce Image Optimization cache (Optional but helps)
  images: {
    unoptimized: true, 
  },
};

module.exports = nextConfig;
