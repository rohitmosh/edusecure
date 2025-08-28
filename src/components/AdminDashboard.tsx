import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Shield, 
  Key, 
  FileCheck, 
  Clock, 
  AlertTriangle, 
  Eye, 
  Calendar,
  Activity,
  Lock,
  Unlock,
  CheckCircle
} from 'lucide-react';

interface AdminDashboardProps {
  username: string;
  onLogout: () => void;
}

const AdminDashboard = ({ username, onLogout }: AdminDashboardProps) => {
  const [selectedExam, setSelectedExam] = useState<string | null>(null);

  // Mock data
  const examPapers = [
    {
      id: 'exam123',
      title: 'Advanced Mathematics Final',
      uploader: 'Dr. Smith',
      uploadTime: '2025-08-28 10:30',
      scheduledTime: '2025-09-01 10:00',
      status: 'scheduled',
      pages: 4,
      integrityStatus: 'verified'
    },
    {
      id: 'exam124',
      title: 'Computer Science Theory',
      uploader: 'Prof. Johnson',
      uploadTime: '2025-08-28 14:15',
      scheduledTime: '2025-09-02 14:00',
      status: 'pending',
      pages: 6,
      integrityStatus: 'verified'
    }
  ];

  const systemLogs = [
    { id: 1, event: 'Paper Upload', user: 'Dr. Smith', exam: 'exam123', time: '10:30', status: 'success' },
    { id: 2, event: 'Integrity Check', user: 'System', exam: 'exam123', time: '10:31', status: 'verified' },
    { id: 3, event: 'Access Attempt', user: 'ExamCenter1', exam: 'exam123', time: '11:00', status: 'denied_early' },
    { id: 4, event: 'Key Schedule', user: 'admin1', exam: 'exam123', time: '11:15', status: 'scheduled' }
  ];

  const handleReleaseKey = (examId: string) => {
    console.log(`Releasing chaos key for exam: ${examId}`);
  };

  const handleVerifyIntegrity = (examId: string) => {
    console.log(`Verifying integrity for exam: ${examId}`);
  };

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-gradient-to-br from-primary to-accent rounded-full flex items-center justify-center">
              <Shield className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-foreground">Admin Dashboard</h1>
              <p className="text-muted-foreground">Welcome, {username}</p>
            </div>
          </div>
          <Button variant="outline" onClick={onLogout}>
            Logout
          </Button>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card className="border-0 shadow-md bg-gradient-to-br from-primary/10 to-primary/5">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Total Papers</p>
                  <p className="text-2xl font-bold text-foreground">12</p>
                </div>
                <FileCheck className="h-8 w-8 text-primary" />
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md bg-gradient-to-br from-accent/10 to-accent/5">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Active Keys</p>
                  <p className="text-2xl font-bold text-foreground">3</p>
                </div>
                <Key className="h-8 w-8 text-accent" />
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md bg-gradient-to-br from-warning/10 to-warning/5">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Pending Release</p>
                  <p className="text-2xl font-bold text-foreground">2</p>
                </div>
                <Clock className="h-8 w-8 text-warning" />
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md bg-gradient-to-br from-destructive/10 to-destructive/5">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Security Alerts</p>
                  <p className="text-2xl font-bold text-foreground">0</p>
                </div>
                <AlertTriangle className="h-8 w-8 text-destructive" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <Tabs defaultValue="papers" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="papers">Exam Papers</TabsTrigger>
            <TabsTrigger value="keys">Key Management</TabsTrigger>
            <TabsTrigger value="logs">Security Logs</TabsTrigger>
          </TabsList>

          <TabsContent value="papers" className="space-y-4">
            <Card className="border-0 shadow-md">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileCheck className="h-5 w-5" />
                  Exam Papers Overview
                </CardTitle>
                <CardDescription>
                  Monitor and manage all uploaded exam papers
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {examPapers.map((exam) => (
                    <div key={exam.id} className="flex items-center justify-between p-4 border border-border rounded-lg bg-card/50">
                      <div className="flex-1">
                        <h3 className="font-semibold text-foreground">{exam.title}</h3>
                        <div className="flex items-center gap-4 mt-2 text-sm text-muted-foreground">
                          <span>Uploaded by: {exam.uploader}</span>
                          <span>Pages: {exam.pages}</span>
                          <span>Upload Time: {exam.uploadTime}</span>
                        </div>
                        <div className="flex items-center gap-2 mt-2">
                          <Badge variant={exam.status === 'scheduled' ? 'default' : 'secondary'}>
                            {exam.status}
                          </Badge>
                          <Badge variant={exam.integrityStatus === 'verified' ? 'default' : 'destructive'}>
                            <CheckCircle className="h-3 w-3 mr-1" />
                            {exam.integrityStatus}
                          </Badge>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Button variant="outline" size="sm" onClick={() => handleVerifyIntegrity(exam.id)}>
                          <Eye className="h-4 w-4 mr-1" />
                          Verify
                        </Button>
                        <Button variant="outline" size="sm">
                          <Calendar className="h-4 w-4 mr-1" />
                          Schedule: {exam.scheduledTime}
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="keys" className="space-y-4">
            <Card className="border-0 shadow-md">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Key className="h-5 w-5" />
                  Chaos Key Management
                </CardTitle>
                <CardDescription>
                  Control the release of decryption keys for scheduled exams
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {examPapers.map((exam) => (
                    <div key={exam.id} className="flex items-center justify-between p-4 border border-border rounded-lg bg-card/50">
                      <div className="flex-1">
                        <h3 className="font-semibold text-foreground">{exam.title}</h3>
                        <p className="text-sm text-muted-foreground">Scheduled: {exam.scheduledTime}</p>
                      </div>
                      <div className="flex items-center gap-2">
                        {exam.status === 'scheduled' ? (
                          <Button 
                            onClick={() => handleReleaseKey(exam.id)}
                            className="bg-gradient-to-r from-accent to-accent-glow"
                          >
                            <Unlock className="h-4 w-4 mr-1" />
                            Release Key
                          </Button>
                        ) : (
                          <Button variant="outline" disabled>
                            <Lock className="h-4 w-4 mr-1" />
                            Key Locked
                          </Button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="logs" className="space-y-4">
            <Card className="border-0 shadow-md">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Activity className="h-5 w-5" />
                  Security Audit Logs
                </CardTitle>
                <CardDescription>
                  Tamper-proof hash-chained activity logs
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {systemLogs.map((log) => (
                    <div key={log.id} className="flex items-center justify-between p-3 border border-border rounded-lg bg-card/30">
                      <div className="flex items-center gap-4">
                        <div className="w-2 h-2 rounded-full bg-accent"></div>
                        <div>
                          <span className="font-medium text-foreground">{log.event}</span>
                          <span className="text-muted-foreground ml-2">by {log.user}</span>
                          {log.exam && (
                            <span className="text-muted-foreground ml-2">on {log.exam}</span>
                          )}
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-sm text-muted-foreground">{log.time}</span>
                        <Badge variant={log.status === 'success' || log.status === 'verified' ? 'default' : 'destructive'}>
                          {log.status}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default AdminDashboard;