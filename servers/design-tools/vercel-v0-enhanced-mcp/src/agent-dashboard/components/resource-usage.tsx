import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { HardDrive, Cpu, Activity } from 'lucide-react'

const resourceData = [
  {
    name: 'Disk Space',
    used: 2.4,
    total: 10,
    unit: 'GB',
    icon: HardDrive,
    color: 'bg-blue-500'
  },