'use client'

import { useState, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Plus, Moon, Sun, CheckCircle2 } from 'lucide-react'
import { Todo, FilterType } from '../types/todo'
import { useLocalStorage } from '../hooks/useLocalStorage'
import { useDarkMode } from '../hooks/useDarkMode'
import { TodoList } from './TodoList'
import { FilterTabs } from './FilterTabs'

export function TodoApp() {
  const [todos, setTodos] = useLocalStorage<Todo[]>('todos', [])
  const [newTodoText, setNewTodoText] = useState('')
  const [activeFilter, setActiveFilter] = useState<FilterType>('all')
  const { isDark, toggleDarkMode } = useDarkMode()

  const filteredTodos = useMemo(() => {
    switch (activeFilter) {
      case 'active':
        return todos.filter(todo => !todo.completed)
      case 'completed':
        return todos.filter(todo => todo.completed)
      default:
        return todos
    }
  }, [todos, activeFilter])

  const counts = useMemo(() => ({
    all: todos.length,
    active: todos.filter(todo => !todo.completed).length,
    completed: todos.filter(todo => todo.completed).length,
  }), [todos])

  const addTodo = () => {
    if (!newTodoText.trim()) return

    const newTodo: Todo = {
      id: crypto.randomUUID(),
      text: newTodoText.trim(),
      completed: false,
      createdAt: new Date(),
      updatedAt: new Date(),
    }

    setTodos(prev => [newTodo, ...prev])
    setNewTodoText('')
  }

  const toggleTodo = (id: string) => {
    setTodos(prev =>
      prev.map(todo =>
        todo.id === id
          ? { ...todo, completed: !todo.completed, updatedAt: new Date() }
          : todo
      )
    )
  }

  const deleteTodo = (id: string) => {
    setTodos(prev => prev.filter(todo => todo.id !== id))
  }

  const editTodo = (id: string, text: string) => {
    setTodos(prev =>
      prev.map(todo =>
        todo.id === id
          ? { ...todo, text, updatedAt: new Date() }
          : todo
      )
    )
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      addTodo()
    }
  }

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="flex items-center justify-between mb-8"
      >
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary text-primary-foreground rounded-lg">
            <CheckCircle2 size={24} />
          </div>
          <div>
            <h1 className="text-2xl font-semibold text-foreground">Tasks</h1>
            <p className="text-sm text-muted-foreground">
              {counts.active} active, {counts.completed} completed
            </p>
          </div>
        </div>
        
        <button
          onClick={toggleDarkMode}
          className="p-2 text-muted-foreground hover:text-foreground hover:bg-muted rounded-lg transition-colors duration-200"
        >
          {isDark ? <Sun size={20} /> : <Moon size={20} />}
        </button>
      </motion.div>

      {/* Add Todo Input */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="mb-6"
      >
        <div className="relative">
          <input
            type="text"
            value={newTodoText}
            onChange={(e) => setNewTodoText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Add a new task..."
            className="w-full px-4 py-3 pl-12 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all duration-200"
          />
          <Plus 
            size={20} 
            className="absolute left-4 top-1/2 transform -translate-y-1/2 text-muted-foreground" 
          />
          {newTodoText.trim() && (
            <motion.button
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              onClick={addTodo}
              className="absolute right-2 top-1/2 transform -translate-y-1/2 px-3 py-1.5 bg-primary text-primary-foreground text-sm rounded-md hover:bg-primary/90 transition-colors duration-200"
            >
              Add
            </motion.button>
          )}
        </div>
      </motion.div>

      {/* Filter Tabs */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="mb-6"
      >
        <FilterTabs
          activeFilter={activeFilter}
          onFilterChange={setActiveFilter}
          counts={counts}
        />
      </motion.div>

      {/* Todo List */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        {todos.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center py-12"
          >
            <div className="w-16 h-16 mx-auto mb-4 bg-muted rounded-full flex items-center justify-center">
              <CheckCircle2 size={32} className="text-muted-foreground" />
            </div>
            <h3 className="text-lg font-medium text-foreground mb-2">No tasks yet</h3>
            <p className="text-muted-foreground">
              Add your first task above to get started
            </p>
          </motion.div>
        ) : filteredTodos.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center py-12"
          >
            <div className="w-16 h-16 mx-auto mb-4 bg-muted rounded-full flex items-center justify-center">
              <CheckCircle2 size={32} className="text-muted-foreground" />
            </div>
            <h3 className="text-lg font-medium text-foreground mb-2">
              No {activeFilter} tasks
            </h3>
            <p className="text-muted-foreground">
              {activeFilter === 'completed' 
                ? 'Complete some tasks to see them here'
                : 'All your tasks are completed!'
              }
            </p>
          </motion.div>
        ) : (
          <TodoList
            todos={filteredTodos}
            onToggle={toggleTodo}
            onDelete={deleteTodo}
            onEdit={editTodo}
          />
        )}
      </motion.div>

      {/* Stats Footer */}
      {todos.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="mt-8 pt-6 border-t border-border"
        >
          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <span>
              {counts.completed} of {counts.all} tasks completed
            </span>
            {counts.completed > 0 && (
              <span>
                {Math.round((counts.completed / counts.all) * 100)}% done
              </span>
            )}
          </div>
          {counts.completed > 0 && (
            <div className="mt-2 w-full bg-muted rounded-full h-1.5">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${(counts.completed / counts.all) * 100}%` }}
                transition={{ duration: 0.5, ease: 'easeOut' }}
                className="bg-primary h-1.5 rounded-full"
              />
            </div>
          )}
        </motion.div>
      )}
    </div>
  )
}