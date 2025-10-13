import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { GitBranch, Clock, Code, TestTube, Eye, AlertCircle } from 'lucide-react'

type AgentStatus = 'coding' | 'testing' | 'waiting' | 'error'

interface Agent {
  id: string
  branch: string
  task: string
  progress: number
  lastCommit: string
  status: AgentStatus
  filesChanged: number
}

const agents: Agent[] = [
  {
    id: 'Agent-001',
    branch: 'feature/user-authentication',
    task: 'Implementing OAuth integration',
    progress: 75,
    lastCommit: '2 minutes ago',
    status: 'coding',
    filesChanged: 8
  },
  {
    id: 'Agent-002',
    branch: 'feature/dashboard-ui',
    task: 'Building responsive dashboard components',
    progress: 90,
    lastCommit: '5 minutes ago',
    status: 'testing',
    filesChanged: 12
  },
  {
    id: 'Agent-003',
    branch: 'fix/memory-leak',
    task: 'Resolving memory leak in data processing',
    progress: 45,
    lastCommit: '1 hour ago',
    status: 'error',
    filesChanged: 3
  },
  {
    id: 'Agent-004',
    branch: 'feature/api-endpoints',
    task: 'Creating REST API endpoints',
    progress: 60,
    lastCommit: '15 minutes ago',
    status: 'coding',
    filesChanged: 6
  },
  {
    id: 'Agent-005',
    branch: 'feature/data-visualization',
    task: 'Implementing chart components',
    progress: 100,
    lastCommit: '30 minutes ago',
    status: 'waiting',
    filesChanged: 15
  },
  {
    id: 'Agent-006',
    branch: 'feature/notification-system',
    task: 'Building real-time notifications',
    progress: 25,
    lastCommit: '45 minutes ago',
    status: 'coding',
    filesChanged: 4
  }
]

const statusConfig = {
  coding: { color: 'bg-blue-500', icon: Code, label: 'Coding' },
  testing: { color: 'bg-yellow-500', icon: TestTube, label: 'Testing' },
  waiting: { color: 'bg-green-500', icon: Eye, label: 'Review' },
  error: { color: 'bg-red-500', icon: AlertCircle, label: 'Error' }
}

export function AgentGrid() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Active Agents</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {agents.map((agent) => {
          const status = statusConfig[agent.status]
          return (
            <Card key={agent.id} className="bg-gray-900/50 border-gray-800 hover:bg-gray-900/70 transition-all duration-200 hover:scale-105">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg font-medium">{agent.id}</CardTitle>
                  <Badge className={`${status.color} text-white border-0`}>
                    <status.icon className="w-3 h-3 mr-1" />
                    {status.label}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center space-x-2 text-sm text-gray-400">
                  <GitBranch className="w-4 h-4" />
                  <span className="truncate">{agent.branch}</span>
                </div>
                
                <div>
                  <p className="text-sm font-medium mb-2">{agent.task}</p>
                  <Progress value={agent.progress} className="h-2" />
                  <p className="text-xs text-gray-400 mt-1">{agent.progress}% complete</p>
                </div>

                <div className="flex items-center justify-between text-xs text-gray-400">
                  <div className="flex items-center space-x-1">
                    <Clock className="w-3 h-3" />
                    <span>{agent.lastCommit}</span>
                  </div>
                  <span>{agent.filesChanged} files changed</span>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}