import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Building2, 
  Download, 
  Unlock, 
  Lock, 
  Clock, 
  FileText, 
  Shield, 
  AlertTriangle,
  CheckCircle,
  Eye,
  Loader2
} from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface ExamCenterViewProps {
  username: string;
  onLogout: () => void;
}

const ExamCenterView = ({ username, onLogout }: ExamCenterViewProps) => {
  const [availableExams, setAvailableExams] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState<string | null>(null);
  const [decrypting, setDecrypting] = useState<string | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    fetchExams();
    // Poll for updates every 30 seconds
    const interval = setInterval(fetchExams, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchExams = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/examcenter/papers', {
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
      
      const response = await fetch(`http://localhost:5000/api/examcenter/download/${examId}`, {
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
      
      const response = await fetch(`http://localhost:5000/api/examcenter/decrypt/${examId}`, {
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
            <Button variant="outline" size="sm" onClick={fetchExams}>
              <Clock className="h-4 w-4 mr-1" />
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
                    {availableExams.filter(exam => !exam.key_released).length}
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
                    {availableExams.filter(exam => exam.key_released).length}
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
              <div className="space-y-4">
                {availableExams.map((exam) => (
                  <div key={exam.exam_id} className="border border-border rounded-lg bg-card/50">
                    <div className="p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <h3 className="font-semibold text-foreground text-lg">{exam.exam_id}</h3>
                          <div className="flex items-center gap-4 mt-2 text-sm text-muted-foreground">
                            <span>Scheduled: {new Date(exam.scheduled_time).toLocaleString()}</span>
                          </div>
                          <div className="flex items-center gap-2 mt-3">
                            <Badge variant={exam.key_released ? 'default' : 'secondary'}>
                              {exam.key_released ? 'Key Released' : 'Scheduled'}
                            </Badge>
                            <Badge variant={exam.key_released ? 'default' : 'destructive'}>
                              {exam.key_released ? 'Key Available' : 'Key Locked'}
                            </Badge>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <Button 
                            variant="outline" 
                            onClick={() => handleDownload(exam.exam_id)}
                            disabled={downloading === exam.exam_id}
                          >
                            {downloading === exam.exam_id ? (
                              <Loader2 className="h-4 w-4 mr-1 animate-spin" />
                            ) : (
                              <Download className="h-4 w-4 mr-1" />
                            )}
                            Download Scrambled
                          </Button>
                          <Button 
                            onClick={() => handleDecrypt(exam.exam_id)}
                            disabled={!exam.key_released || decrypting === exam.exam_id}
                            className="bg-gradient-to-r from-accent to-accent-glow disabled:from-muted disabled:to-muted"
                          >
                            {decrypting === exam.exam_id ? (
                              <Loader2 className="h-4 w-4 mr-1 animate-spin" />
                            ) : exam.key_released ? (
                              <Eye className="h-4 w-4 mr-1" />
                            ) : (
                              <Lock className="h-4 w-4 mr-1" />
                            )}
                            {exam.key_released ? 'Decrypt Paper' : 'Locked'}
                          </Button>
                        </div>
                      </div>
                    </div>

                    {/* Visual Preview */}
                    <div className="border-t border-border p-4 bg-muted/20">
                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label className="text-sm font-medium flex items-center gap-1">
                            <AlertTriangle className="h-3 w-3 text-destructive" />
                            Scrambled (Downloaded)
                          </Label>
                          <div className="aspect-[4/3] bg-gradient-to-br from-red-100 to-red-200 rounded border-2 border-red-300 flex items-center justify-center">
                            <div className="text-center">
                              <Shield className="h-6 w-6 mx-auto mb-1 text-red-600" />
                              <p className="text-xs text-red-600 font-medium">ENCRYPTED</p>
                              <div className="mt-2 grid grid-cols-6 gap-1">
                                {Array.from({ length: 24 }).map((_, i) => (
                                  <div key={i} className="h-1 bg-red-400 rounded" style={{
                                    transform: `rotate(${Math.random() * 360}deg)`,
                                    opacity: Math.random()
                                  }}></div>
                                ))}
                              </div>
                            </div>
                          </div>
                        </div>

                        <div className="space-y-2">
                          <Label className="text-sm font-medium flex items-center gap-1">
                            {exam.key_released ? (
                              <>
                                <CheckCircle className="h-3 w-3 text-accent" />
                                Original (Decrypted)
                              </>
                            ) : (
                              <>
                                <Lock className="h-3 w-3 text-muted-foreground" />
                                Original (Locked)
                              </>
                            )}
                          </Label>
                          <div className={`aspect-[4/3] rounded border-2 flex items-center justify-center transition-all duration-500 ${
                            exam.key_released 
                              ? 'bg-gradient-to-br from-green-100 to-green-200 border-green-300' 
                              : 'bg-muted border-muted-foreground/20 blur-sm'
                          }`}>
                            <div className="text-center p-2">
                              {exam.key_released ? (
                                <>
                                  <FileText className="h-6 w-6 mx-auto mb-1 text-green-600" />
                                  <p className="text-xs text-green-600 font-medium">READABLE</p>
                                  <div className="mt-2 space-y-1">
                                    <div className="h-1 bg-green-500 rounded w-3/4 mx-auto"></div>
                                    <div className="h-1 bg-green-500 rounded w-full mx-auto"></div>
                                    <div className="h-1 bg-green-500 rounded w-2/3 mx-auto"></div>
                                    <div className="h-1 bg-green-500 rounded w-5/6 mx-auto"></div>
                                  </div>
                                </>
                              ) : (
                                <>
                                  <Lock className="h-6 w-6 mx-auto mb-1 text-muted-foreground" />
                                  <p className="text-xs text-muted-foreground">AWAITING KEY</p>
                                </>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
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