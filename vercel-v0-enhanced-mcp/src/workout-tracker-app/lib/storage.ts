import { Exercise, DayWorkout, WorkoutStats } from './types'

const STORAGE_KEY = 'workout-tracker-data'

export function saveExercise(exercise: Exercise): void {
  const data = getStorageData()
  data.exercises.push(exercise)
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
}

export function updateExercise(exerciseId: string, updates: Partial<Exercise>): void {
  const data = getStorageData()
  const index = data.exercises.findIndex(ex => ex.id === exerciseId)
  if (index !== -1) {
    data.exercises[index] = { ...data.exercises[index], ...updates }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
  }
}

export function deleteExercise(exerciseId: string): void {
  const data = getStorageData()
  data.exercises = data.exercises.filter(ex => ex.id !== exerciseId)
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
}

export function getExercisesByDate(date: string): Exercise[] {
  const data = getStorageData()
  return data.exercises.filter(ex => ex.date === date)
}

export function getTodaysExercises(): Exercise[] {
  const today = new Date().toDateString()
  return getExercisesByDate(today)
}

export function getWorkoutHistory(days: number = 7): DayWorkout[] {
  const history: DayWorkout[] = []
  
  for (let i = 0; i < days; i++) {
    const date = new Date()
    date.setDate(date.getDate() - i)
    const dateString = date.toDateString()
    
    const exercises = getExercisesByDate(dateString)
    const stats = calculateWorkoutStats(exercises)
    
    history.push({
      date: dateString,
      exercises,
      stats
    })
  }
  
  return history
}

export function calculateWorkoutStats(exercises: Exercise[]): WorkoutStats {
  return {
    totalExercises: exercises.length,
    totalSets: exercises.reduce((sum, ex) => sum + ex.sets, 0),
    totalVolume: exercises.reduce((sum, ex) => sum + (ex.sets * ex.reps * ex.weight), 0)
  }
}

function getStorageData(): { exercises: Exercise[] } {
  if (typeof window === 'undefined') {
    return { exercises: [] }
  }
  
  const stored = localStorage.getItem(STORAGE_KEY)
  if (!stored) {
    return { exercises: [] }
  }
  
  try {
    return JSON.parse(stored)
  } catch {
    return { exercises: [] }
  }
}

export const commonExercises = [
  'Bench Press',
  'Squats',
  'Deadlift',
  'Overhead Press',
  'Barbell Row',
  'Pull-ups',
  'Chin-ups',
  'Dips',
  'Incline Bench Press',
  'Decline Bench Press',
  'Dumbbell Press',
  'Dumbbell Flyes',
  'Lat Pulldown',
  'Seated Row',
  'Leg Press',
  'Leg Curls',
  'Leg Extensions',
  'Calf Raises',
  'Bicep Curls',
  'Tricep Extensions',
  'Shoulder Press',
  'Lateral Raises',
  'Front Raises',
  'Shrugs',
  'Planks',
  'Push-ups',
  'Lunges',
  'Hip Thrusts',
  'Romanian Deadlift',
  'Sumo Deadlift'
]