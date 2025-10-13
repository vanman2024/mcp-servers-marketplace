import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diffInMs = now.getTime() - date.getTime()
  const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24))

  if (diffInDays === 0) {
    return 'Today'
  } else if (diffInDays === 1) {
    return 'Yesterday'
  } else if (diffInDays < 7) {
    return `${diffInDays} days ago`
  } else {
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }
}

export function formatDuration(minutes: number): string {
  if (minutes < 60) {
    return `${minutes}m`
  }
  const hours = Math.floor(minutes / 60)
  const remainingMinutes = minutes % 60
  return remainingMinutes > 0 ? `${hours}h ${remainingMinutes}m` : `${hours}h`
}

export function calculateVolume(sets: Array<{ reps: number; weight: number }>): number {
  return sets.reduce((total, set) => total + (set.reps * set.weight), 0)
}

export function getWeekStart(date: Date): Date {
  const weekStart = new Date(date)
  weekStart.setDate(date.getDate() - date.getDay())
  weekStart.setHours(0, 0, 0, 0)
  return weekStart
}

export function getMonthStart(date: Date): Date {
  const monthStart = new Date(date.getFullYear(), date.getMonth(), 1)
  monthStart.setHours(0, 0, 0, 0)
  return monthStart
}

export function isDateInRange(dateString: string, startDate: Date, endDate: Date): boolean {
  const date = new Date(dateString)
  return date >= startDate && date <= endDate
}

export function groupWorkoutsByWeek(workouts: Array<{ date: string }>): Record<string, number> {
  const weeks: Record<string, number> = {}
  
  workouts.forEach(workout => {
    const date = new Date(workout.date)
    const weekStart = getWeekStart(date)
    const weekKey = weekStart.toISOString().split('T')[0]
    
    weeks[weekKey] = (weeks[weekKey] || 0) + 1
  })

  return weeks
}

export function groupWorkoutsByMonth(workouts: Array<{ date: string }>): Record<string, number> {
  const months: Record<string, number> = {}
  
  workouts.forEach(workout => {
    const date = new Date(workout.date)
    const monthStart = getMonthStart(date)
    const monthKey = monthStart.toISOString().split('T')[0]
    
    months[monthKey] = (months[monthKey] || 0) + 1
  })

  return months
}

export function findPersonalRecords(workouts: Array<{
  date: string
  exercises: Array<{
    name: string
    sets: Array<{ reps: number; weight: number }>
  }>
}>): Record<string, { weight: number; reps: number; date: string }> {
  const records: Record<string, { weight: number; reps: number; date: string }> = {}
  
  workouts.forEach(workout => {
    workout.exercises.forEach(exercise => {
      exercise.sets.forEach(set => {
        const currentRecord = records[exercise.name]
        
        if (!currentRecord || set.weight > currentRecord.weight || 
            (set.weight === currentRecord.weight && set.reps > currentRecord.reps)) {
          records[exercise.name] = {
            weight: set.weight,
            reps: set.reps,
            date: workout.date
          }
        }
      })
    })
  })
  
  return records
}

export function calculateWorkoutStats(workouts: Array<{
  date: string
  exercises: Array<{
    name: string
    sets: Array<{ reps: number; weight: number }>
  }>
  duration?: number
}>): {
  totalWorkouts: number
  totalExercises: number
  totalSets: number
  totalVolume: number
  averageWorkoutDuration?: number
  workoutsThisWeek: number
  workoutsThisMonth: number
} {
  const now = new Date()
  const weekStart = getWeekStart(now)
  const monthStart = getMonthStart(now)
  
  const totalWorkouts = workouts.length
  const totalExercises = workouts.reduce((sum, workout) => sum + workout.exercises.length, 0)
  const totalSets = workouts.reduce((sum, workout) => 
    sum + workout.exercises.reduce((exerciseSum, exercise) => exerciseSum + exercise.sets.length, 0), 0
  )
  const totalVolume = workouts.reduce((sum, workout) => 
    sum + workout.exercises.reduce((exerciseSum, exercise) => 
      exerciseSum + calculateVolume(exercise.sets), 0
    ), 0
  )
  
  const workoutsWithDuration = workouts.filter(w => w.duration !== undefined)
  const averageWorkoutDuration = workoutsWithDuration.length > 0
    ? workoutsWithDuration.reduce((sum, w) => sum + (w.duration || 0), 0) / workoutsWithDuration.length
    : undefined
  
  const workoutsThisWeek = workouts.filter(workout => 
    isDateInRange(workout.date, weekStart, now)
  ).length
  
  const workoutsThisMonth = workouts.filter(workout => 
    isDateInRange(workout.date, monthStart, now)
  ).length
  
  return {
    totalWorkouts,
    totalExercises,
    totalSets,
    totalVolume,
    averageWorkoutDuration,
    workoutsThisWeek,
    workoutsThisMonth
  }
}