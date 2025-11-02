# Image Generation Output Configuration

## Where Generated Images Go

The `content-image-generation` MCP server saves generated images based on the `OUTPUT_DIR` environment variable.

## Configuration by Project Type

### Next.js Projects (`nextjs-frontend` plugin)
```json
"OUTPUT_DIR": "./public/images/generated"
```

**Result**: Images save to `your-nextjs-app/public/images/generated/`
- Accessible at: `/images/generated/imagen3_20250101_120000.png`
- Use in Next.js: `<Image src="/images/generated/..." />`

### Astro Projects (`website-builder` plugin)
```json
"OUTPUT_DIR": "./public/images/generated"
```

**Result**: Images save to `your-astro-site/public/images/generated/`
- Accessible at: `/images/generated/imagen3_20250101_120000.png`
- Use in Astro: `<img src="/images/generated/..." />`

## How It Works

### 1. When You Generate an Image

```bash
/website-builder:generate-images "hero background"
```

### 2. MCP Server Creates Image

- Calls Google Imagen API
- Generates image
- Saves to `OUTPUT_DIR` (resolves to `./public/images/generated` relative to your project)

### 3. Returns File Path

```json
{
  "success": true,
  "image_path": "/absolute/path/to/your-project/public/images/generated/imagen3_20250101_120000.png",
  "filename": "imagen3_20250101_120000.png"
}
```

### 4. Plugin Uses the Image

The plugin automatically:
- Reads the returned filename
- Inserts into your component/page code
- Uses web path: `/images/generated/imagen3_20250101_120000.png`

## Manual Configuration

If you need custom output location, set in your project's `.env`:

```env
OUTPUT_DIR=/custom/path/to/images
```

Or update the plugin's `.mcp.json`:

```json
{
  "content-image-generation": {
    "env": {
      "OUTPUT_DIR": "/custom/output/path"
    }
  }
}
```

## Database Storage (Optional)

Generated images can ALSO be uploaded to Supabase Storage after creation:

### 1. Generate Image (saves to filesystem)
```bash
/website-builder:generate-images "product photo"
```

### 2. Upload to Supabase Storage (optional)
```typescript
// Plugin can automatically upload
const supabase = createClient()
await supabase.storage
  .from('generated-images')
  .upload('product-photo.png', imageFile)
```

### 3. Save URL to Database
```sql
INSERT INTO media (filename, url, type)
VALUES ('product-photo.png', 'https://...supabase.co/storage/.../product-photo.png', 'generated')
```

## Best Practices

### Local Development
```
OUTPUT_DIR=./public/images/generated
```
- Images in your project's public folder
- Committed to git (or gitignored)
- Instant preview in development

### Production
**Option 1: Filesystem** (Simple)
- Same as development
- Images stored in deployment (Vercel, Netlify, etc.)
- Fast access, no extra storage costs

**Option 2: Supabase Storage** (Scalable)
- Generate to temp folder
- Upload to Supabase Storage
- Store URL in database
- CDN-backed, persistent across deployments

## Example Workflow

### Website Builder (Astro)
```bash
# 1. Generate hero image
/website-builder:generate-images "modern SaaS hero background"

# 2. Plugin creates:
# - File: ./public/images/generated/imagen3_20250101_120000.png
# - Component code with: src="/images/generated/imagen3_20250101_120000.png"

# 3. Build & deploy
npm run build

# 4. Image included in static build
```

### Next.js Frontend
```bash
# 1. Generate product images
/nextjs-frontend:add-component product-gallery

# 2. Generate images for products
# MCP generates to: ./public/images/generated/

# 3. Component uses Next.js Image:
<Image
  src="/images/generated/product-1.png"
  width={800}
  height={600}
  alt="Product"
/>

# 4. Deploy - Vercel serves from public/
```

## Troubleshooting

### Images not appearing?
1. Check `OUTPUT_DIR` is set correctly
2. Verify directory exists: `mkdir -p ./public/images/generated`
3. Check file permissions
4. Confirm path is relative to project root

### Want to change location mid-project?
1. Update `.mcp.json` with new `OUTPUT_DIR`
2. Restart Claude Code to reload MCP config
3. Move existing images: `mv ./public/images/generated ./new/path`

## Summary

**Default Setup** (Current):
- ✅ Images save to `./public/images/generated`
- ✅ Accessible via `/images/generated/filename.png`
- ✅ Works for both Next.js and Astro
- ✅ No database required
- ✅ Fast and simple

**Optional Enhancements**:
- Upload to Supabase Storage for CDN
- Store metadata in database
- Auto-optimization and transforms
