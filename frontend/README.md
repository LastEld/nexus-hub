# NexusHub Frontend

Modern Next.js 15 frontend with TypeScript and shadcn/ui.

## Features

- ⚡️ Next.js 15 with App Router
- 🎨 shadcn/ui components
- 🎭 Dark mode support
- 📱 Fully responsive
- 🔒 Type-safe with TypeScript
- 🎯 React Query for data fetching
- 🎨 Tailwind CSS for styling
- 📝 Zod for validation

## Getting Started

```bash
# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
src/
├── app/              # Next.js App Router pages
├── components/       # Shared components
│   ├── ui/          # shadcn/ui components
│   └── common/      # App-specific components
├── features/        # Feature modules
├── lib/             # Utilities and helpers
└── types/           # TypeScript types
```

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - TypeScript type checking
