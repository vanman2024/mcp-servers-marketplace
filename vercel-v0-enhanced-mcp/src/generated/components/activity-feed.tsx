import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { GitBranch, GitCommit, GitPullRequest, FileText } from 'lucide-react'

interface Activity {
  id: string
  agent: string
  action: string
  details: string
  timestamp: string
  type: 'branch' | 'commit' | 'pr' | 'file'
}

const activities: Activity[] = [
  {
    id: '1',
    agent: 'Agent-003',
    action: 'created new branch',
    details: 'feature/user-auth',
    timestamp: '2 min ago',
    type: 'branch'
  },
  {
    id: '2',
    agent: 'Agent-001',
    action: 'pushed 3 commits to',
    details: 'feature/dashboard',
    timestamp: '5 min ago',
    type: 'commit'
  },
  {
    id: '3',
    agent: 'Agent-005',
    action: 'opened pull request',
    details: '#47: Add data visualization',
    timestamp: '8 min ago',
    type: 'pr'
  },
  {
    id: '4',
    agent: 'Agent-002',
    action: 'modified file',
    details: 'components/dashboard.tsx',
    timestamp: '12 min ago',
    type: 'file'
  },
  {
    id: '5',
    agent: 'Agent-004',
    action: 'merged pull request',
    details: '#45: Fix authentication bug',
    timestamp: '15 min ago',
    type: 'pr'
  },
  {
    id: '6',
    agent: 'Agent-006',
    action: 'created new branch',
    details: 'hotfix/critical-security',
    timestamp: '18 min ago',
    type: 'branch'
  }
]

const typeConfig = {
  branch: { icon: GitBranch, color: 'text-blue-400' },
  commit: { icon: GitCommit, color: 'text-green-400' },
  pr: { icon: GitPullRequest, color: 'text-purple-400' },
  file: { icon: FileText, color: 'text-yellow-400' }
}

export function ActivityFeed() {
  return (
    <Card className="bg-gray-900/50 border-gray-800">
      <CardHeader>
        <CardTitle className="text-lg">Live Activity Feed</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4 max-h-96 overflow-y-auto">
        {activities.map((activity) => {
          const config = typeConfig[activity.type]
          return (
            <div key={activity.id} className="flex items-start space-x-3 p-3 rounded-lg bg-gray-800/50 hover:bg-gray-800/70 transition-colors">
              <config.icon className={`w-4 h-4 mt-0.5 ${config.color}`} />
              <div className="flex-1 min-w-0">
                <p className="text-sm">
                  <span className="font-medium text-blue-400">{activity.agent}</span>
                  <span className="text-gray-300"> {activity.action} </span>
                  <span className="font-medium">{activity.details}</span>
                </p>
                <p className="text-xs text-gray-400 mt-1">{activity.timestamp}</p>
              </div>
            </div>
          )
        })}
      </CardContent>
    </Card>
  )
}