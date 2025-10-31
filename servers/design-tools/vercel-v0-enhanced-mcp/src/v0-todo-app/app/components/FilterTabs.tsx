'use client'

import { motion } from 'framer-motion'
import { FilterType } from '../types/todo'

interface FilterTabsProps {
  activeFilter: FilterType
  onFilterChange: (filter: FilterType) => void
  counts: {
    all: number
    active: number
    completed: number
  }
}

const filters: { key: FilterType; label: string }[] = [
  { key: 'all', label: 'All' },
  { key: 'active', label: 'Active' },
  { key: 'completed', label: 'Completed' },
]

export function FilterTabs({ activeFilter, onFilterChange, counts }: FilterTabsProps) {
  return (
    <div className="flex bg-muted rounded-lg p-1">
      {filters.map((filter) => (
        <button
          key={filter.key}
          onClick={() => onFilterChange(filter.key)}
          className={`relative flex-1 px-4 py-2 text-sm font-medium rounded-md transition-colors duration-200 ${
            activeFilter === filter.key
              ? 'text-foreground'
              : 'text-muted-foreground hover:text-foreground'
          }`}
        >
          {activeFilter === filter.key && (
            <motion.div
              layoutId="activeTab"
              className="absolute inset-0 bg-background shadow-sm rounded-md"
              transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
            />
          )}
          <span className="relative flex items-center justify-center gap-2">
            {filter.label}
            <span className="text-xs text-muted-foreground bg-muted-foreground/10 px-1.5 py-0.5 rounded-full min-w-[20px] text-center">
              {counts[filter.key]}
            </span>
          </span>
        </button>
      ))}
    </div>
  )
}