export interface WorkoutSet {
  reps: number
  weight: number
  notes?: string
}

export interface Exercise {
  name: string
  sets: WorkoutSet[]
  notes?: string
}

export interface Workout {
  date: string // ISO string
  exercises: Exercise[]
  notes?: string
  duration?: number // in minutes
}

export interface WorkoutStats {
  totalWorkouts: number
  totalExercises: number
  totalSets: number
  totalVolume: number // total weight lifted
  averageWorkoutDuration?: number
  workoutsThisWeek: number
  workoutsThisMonth: number
}

export interface ExerciseProgress {
  exerciseName: string
  sessions: Array<{
    date: string
    maxWeight: number
    totalVolume: number
    totalReps: number
    sets: number
  }>
}

export interface PersonalRecord {
  exerciseName: string
  weight: number
  reps: number
  date: string
}