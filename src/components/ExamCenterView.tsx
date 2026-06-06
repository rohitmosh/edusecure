import { useState, useEffect } from 'react';
import { API_BASE_URL } from '@/config';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Building2,
  Download,
  Lock,
  Clock,
  FileText,
  Shield,
  AlertTriangle,
  CheckCircle,
  Eye,
  Loader2,
  Unlock,
  Key,
  RefreshCw,
  FileDown,
  Image as ImageIcon,
  PlayCircle
} from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import ImagePreview from './ImagePreview';

interface ExamCenterViewProps {
  username: string;
  onLogout: () => void;
}

const ExamCenterView = ({ username, onLogout }: ExamCenterViewProps) => {
  const [availableExams, setAvailableExams] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState<string | null>(null);
  const [decrypting, setDecrypting] = useState<string | null>(null);
  const [simulatingUnlock, setSimulatingUnlock] = useState<string | null>(null);
  const [simulatedUnlocked, setSimulatedUnlocked] = useState<Set<string>>(new Set());
  const { toast } = useToast();

  useEffect(() => {
    fetchExams();
    // Poll for updates every 10 seconds for real-time updates
    const interval = setInterval(fetchExams, 10000);
    return () => clearInterval(interval);
  }, []);

  const fetchExams = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/examcenter/papers`, {
        credentials: 'include'
      });

      if (response.ok) {
        const data = await response.json();
        setAvailableExams(data.papers || []);
      } else {
        toast({
          title: "Error",
          description: "Failed to fetch exam papers",
          variant: "destructive"
        });
      }
    } catch (error) {
      toast({
        title: "Connection Error",
        description: "Unable to connect to server",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (examId: string) => {
    try {
      setDownloading(examId);

      const response = await fetch(`${API_BASE_URL}/api/examcenter/download/${examId}`, {
        credentials: 'include'
      });

      const data = await response.json();

      if (response.ok && data.success) {
        toast({
          title: "Download Complete",
          description: `Scrambled paper downloaded. ${data.total_pages} pages ready.`,
        });
        fetchExams(); // Refresh data
      } else {
        toast({
          title: "Download Failed",
          description: data.error || 'Failed to download paper',
          variant: "destructive"
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to download paper",
        variant: "destructive"
      });
    } finally {
      setDownloading(null);
    }
  };

  const handleDecrypt = async (examId: string) => {
    try {
      setDecrypting(examId);

      const response = await fetch(`${API_BASE_URL}/api/examcenter/decrypt/${examId}`, {
        method: 'POST',
        credentials: 'include'
      });

      const data = await response.json();

      if (response.ok && data.success) {
        toast({
          title: "Paper Decrypted",
          description: `Original exam paper is now readable! ${data.total_pages} pages decrypted.`,
        });
        fetchExams(); // Refresh data
      } else {
        toast({
          title: "Decryption Failed",
          description: data.error || 'Failed to decrypt paper',
          variant: "destructive"
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to decrypt paper",
        variant: "destructive"
      });
    } finally {
      setDecrypting(null);
    }
  };

  const handleSimulateUnlock = async (examId: string) => {
    try {
      setSimulatingUnlock(examId);
      
      // Simulate the unlock process with visual feedback
      toast({
        title: "Simulating Key Release",
        description: "Demonstrating the unlock process...",
      });

      // Wait for 2 seconds to simulate the process
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Add to simulated unlocked set
      setSimulatedUnlocked(prev => new Set([...prev, examId]));

      toast({
        title: "Simulation Complete",
        description: "Key has been simulated as released! You can now view the original paper.",
      });

    } catch (error) {
      toast({
        title: "Simulation Error",
        description: "Failed to simulate unlock",
        variant: "destructive"
      });
    } finally {
      setSimulatingUnlock(null);
    }
  };

  const handleDownloadScrambled = async (examId: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/preview/scrambled/${examId}/1`, {
        credentials: 'include'
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${examId}_scrambled_page_1.png`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        toast({
          title: "Download Started",
          description: "Scrambled image download started",
        });
      } else {
        throw new Error('Download failed');
      }
    } catch (error) {
      toast({
        title: "Download Failed",
        description: "Failed to download scrambled image",
        variant: "destructive"
      });
    }
  };

  const handleDownloadOriginal = async (examId: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/preview/original/${examId}/1`, {
        credentials: 'include'
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${examId}_original_page_1.png`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        toast({
          title: "Download Started",
          description: "Original image download started",
        });
      } else {
        throw new Error('Download failed');
      }
    } catch (error) {
      toast({
        title: "Download Failed",
        description: "Failed to download original image",
        variant: "destructive"
      });
    }
  };

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-gradient-to-br from-primary to-accent rounded-full flex items-center justify-center">
              <Building2 className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-foreground">Exam Center Portal</h1>
              <p className="text-muted-foreground">Welcome, {username}</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" onClick={fetchExams} disabled={loading}>
              {loading ? (
                <Loader2 className="h-4 w-4 mr-1 animate-spin" />
              ) : (
                <RefreshCw className="h-4 w-4 mr-1" />
              )}
              Refresh
            </Button>
            <Button variant="outline" onClick={onLogout}>
              Logout
            </Button>
          </div>
        </div>

        {/* Status Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="border-0 shadow-md bg-gradient-to-br from-primary/10 to-primary/5">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Available Exams</p>
                  <p className="text-2xl font-bold text-foreground">{availableExams.length}</p>
                </div>
                <FileText className="h-8 w-8 text-primary" />
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md bg-gradient-to-br from-warning/10 to-warning/5">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Awaiting Keys</p>
                  <p className="text-2xl font-bold text-foreground">
                    {availableExams.filter(exam => !exam.key_released && !simulatedUnlocked.has(exam.exam_id)).length}
                  </p>
                </div>
                <Clock className="h-8 w-8 text-warning" />
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md bg-gradient-to-br from-accent/10 to-accent/5">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Ready to View</p>
                  <p className="text-2xl font-bold text-foreground">
                    {availableExams.filter(exam => exam.key_released || simulatedUnlocked.has(exam.exam_id)).length}
                  </p>
                </div>
                <CheckCircle className="h-8 w-8 text-accent" />
              </div>
            </CardContent>
          </Card>


        </div>

        {/* Exam Papers List */}
        <Card className="border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              Secure Exam Papers
            </CardTitle>
            <CardDescription>
              Download scrambled papers and decrypt when keys are released
            </CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="flex items-center justify-center p-8">
                <Loader2 className="h-8 w-8 animate-spin" />
              </div>
            ) : availableExams.length === 0 ? (
              <div className="text-center p-8 text-muted-foreground">
                No exam papers available
              </div>
            ) : (
              <div className="space-y-6">
                {availableExams.map((exam) => {
                  const isUnlocked = exam.key_released || simulatedUnlocked.has(exam.exam_id);
                  const isSimulated = simulatedUnlocked.has(exam.exam_id);
                  
                  return (
                    <div key={exam.exam_id} className="border border-border rounded-lg bg-card/50 overflow-hidden">
                      <div className="p-6">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center gap-3 mb-2">
                              <h3 className="font-semibold text-foreground text-xl">{exam.exam_id}</h3>
                              {isSimulated && (
                                <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                                  <PlayCircle className="h-3 w-3 mr-1" />
                                  Demo Mode
                                </Badge>
                              )}
                            </div>
                            <div className="flex items-center gap-4 mt-2 text-sm text-muted-foreground">
                              <span>📅 Scheduled: {new Date(exam.scheduled_time).toLocaleString()}</span>
                              <span>📄 Exam Paper</span>
                              {exam.uploader && <span>👨‍🏫 By: {exam.uploader}</span>}
                            </div>
                            <div className="flex items-center gap-2 mt-4">
                              <Badge variant={isUnlocked ? 'default' : 'secondary'}>
                                {isUnlocked ? 'Unlocked' : 'Locked'}
                              </Badge>
                              <Badge variant={isUnlocked ? 'default' : 'destructive'}>
                                {isUnlocked ? 'Key Available' : 'Key Pending'}
                              </Badge>
                              {exam.key_released && (
                                <Badge variant="outline" className="bg-blue-50 text-blue-700">
                                  Official Release
                                </Badge>
                              )}
                            </div>
                          </div>
                          
                          {/* Action Buttons */}
                          <div className="flex flex-col gap-2 min-w-[200px]">
                            {/* Simulate Unlock Button */}
                            {!exam.key_released && !isSimulated && (
                              <Button
                                variant="outline"
                                onClick={() => handleSimulateUnlock(exam.exam_id)}
                                disabled={simulatingUnlock === exam.exam_id}
                                className="bg-gradient-to-r from-green-50 to-green-100 border-green-200 hover:from-green-100 hover:to-green-200"
                              >
                                {simulatingUnlock === exam.exam_id ? (
                                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                                ) : (
                                  <PlayCircle className="h-4 w-4 mr-2" />
                                )}
                                Simulate Unlock
                              </Button>
                            )}
                            
                            {/* Download Buttons */}
                            <div className="flex gap-2">
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => handleDownloadScrambled(exam.exam_id)}
                                className="flex-1"
                              >
                                <Download className="h-3 w-3 mr-1" />
                                Scrambled
                              </Button>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => handleDownloadOriginal(exam.exam_id)}
                                disabled={!isUnlocked}
                                className="flex-1"
                              >
                                <FileDown className="h-3 w-3 mr-1" />
                                Original
                              </Button>
                            </div>
                            
                            {/* Main Action Button */}
                            <Button
                              onClick={() => handleDecrypt(exam.exam_id)}
                              disabled={!exam.key_released || decrypting === exam.exam_id}
                              className="bg-gradient-to-r from-accent to-accent-glow disabled:from-muted disabled:to-muted"
                            >
                              {decrypting === exam.exam_id ? (
                                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                              ) : isUnlocked ? (
                                <Eye className="h-4 w-4 mr-2" />
                              ) : (
                                <Lock className="h-4 w-4 mr-2" />
                              )}
                              {isUnlocked ? 'View Paper' : 'Awaiting Key'}
                            </Button>
                          </div>
                        </div>
                      </div>

                      {/* Enhanced Image Preview */}
                      <div className="border-t border-border bg-muted/10">
                        <div className="p-4">
                          <div className="flex items-center justify-between mb-4">
                            <h4 className="font-medium text-foreground flex items-center gap-2">
                              <ImageIcon className="h-4 w-4" />
                              Paper Preview
                            </h4>
                            <div className="flex items-center gap-2 text-sm text-muted-foreground">
                              <Shield className="h-4 w-4" />
                              {isUnlocked ? 'Decrypted View Available' : 'Encrypted Content Only'}
                            </div>
                          </div>
                          <ImagePreview
                            examId={exam.exam_id}
                            keyReleased={isUnlocked}
                          />
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Security Notice */}
        <Card className="border-0 shadow-md bg-gradient-to-r from-primary/5 to-accent/5">
          <CardContent className="p-4">
            <div className="flex items-start gap-3">
              <Shield className="h-5 w-5 text-primary mt-0.5" />
              <div>
                <h4 className="font-semibold text-foreground">Security Notice</h4>
                <p className="text-sm text-muted-foreground mt-1">
                  All exam papers are protected by chaotic pixel scrambling. Papers remain unreadable until
                  the admin releases the chaos key at the scheduled exam time. Any attempt to access papers
                  before the scheduled time will be logged and reported.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

const Label = ({ className, children, ...props }: { className?: string; children: React.ReactNode }) => (
  <label className={`text-sm font-medium ${className}`} {...props}>
    {children}
  </label>
);

export default ExamCenterView;