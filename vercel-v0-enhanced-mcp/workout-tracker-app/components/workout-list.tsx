'use client'

import { Workout } from '@/lib/types'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Edit, Trash2 } from 'lucide-react'
import { Badge } from '@/components/ui/badge'

interface WorkoutListProps {
  workouts: Workout[]
  onEdit: (workout: Workout) => void
  onDelete: (id: string) => void
}

export function WorkoutList({ workouts, onEdit, onDelete }: WorkoutListProps) {
  if (workouts.length === 0) {
    return (
      <Card>
        <CardContent className="flex items-center justify-center py-12">
          <p className="text-muted-foreground">No workouts recorded today. Add your first exercise!</p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          Today's Exercises
          <Badge variant="secondary">{workouts.length} exercises</Badge>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Exercise</TableHead>
                <TableHead className="text-center">Sets</TableHead>
                <TableHead className="text-center">Reps</TableHead>
                <TableHead className="text-center">Weight (lbs)</TableHead>
                <TableHead className="text-center">Volume</TableHead>
                <TableHead className="text-center">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {workouts.map((workout) => (
                <TableRow key={workout.id}>
                  <TableCell className="font-medium">{workout.exercise}</TableCell>
                  <TableCell className="text-center">{workout.sets}</TableCell>
                  <TableCell className="text-center">{workout.reps}</TableCell>
                  <TableCell className="text-center">{workout.weight}</TableCell>
                  <TableCell className="text-center font-medium">
                    {(workout.sets * workout.reps * workout.weight).toLocaleString()}
                  </TableCell>
                  <TableCell className="text-center">
                    <div className="flex justify-center gap-2">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => onEdit(workout)}
                      >
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => onDelete(workout.id)}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  )
}