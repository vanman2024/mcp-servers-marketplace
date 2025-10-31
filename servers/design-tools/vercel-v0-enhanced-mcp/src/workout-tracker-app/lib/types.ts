export interface Exercise {
  id: string
  name: string
  sets: number
  reps: number
  weight: number
  date: string
  createdAt: number
}

export interface WorkoutStats {
  totalExercises: number
  totalSets: number
  totalVolume: number
}

export interface DayWorkout {
  date: string
  exercises: Exercise[]
  stats: WorkoutStats
}