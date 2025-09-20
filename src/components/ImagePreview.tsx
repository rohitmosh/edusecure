import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  ChevronLeft, 
  ChevronRight, 
  Eye, 
  EyeOff, 
  Loader2,
  AlertTriangle,
  CheckCircle,
  Lock,
  FileText,
  Shield
} from 'lucide-react';

interface ImagePreviewProps {
  examId: string;
  keyReleased: boolean;
  className?: string;
}

const ImagePreview = ({ examId, keyReleased, className = '' }: ImagePreviewProps) => {
  const [previewInfo, setPreviewInfo] = useState<any>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [showOriginal, setShowOriginal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [imageLoading, setImageLoading] = useState(false);

  useEffect(() => {
    fetchPreviewInfo();
  }, [examId]);

  const fetchPreviewInfo = async () => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:5000/api/preview/info/${examId}`, {
        credentials: 'include'
      });

      if (response.ok) {
        const data = await response.json();
        setPreviewInfo(data);
        if (data.total_pages > 0) {
          setCurrentPage(1);
        }
      }
    } catch (error) {
      console.error('Failed to fetch preview info:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (newPage: number) => {
    if (newPage >= 1 && newPage <= (previewInfo?.total_pages || 0)) {
      setCurrentPage(newPage);
      setImageLoading(true);
    }
  };

  const handleImageLoad = () => {
    setImageLoading(false);
  };

  const handleImageError = () => {
    setImageLoading(false);
  };

  if (loading) {
    return (
      <div className={`flex items-center justify-center p-8 ${className}`}>
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  if (!previewInfo || previewInfo.total_pages === 0) {
    return (
      <div className={`text-center p-8 text-muted-foreground ${className}`}>
        No preview available
      </div>
    );
  }

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Controls */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Badge variant="outline">
            Page {currentPage} of {previewInfo.total_pages}
          </Badge>
          {keyReleased && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowOriginal(!showOriginal)}
              className="flex items-center gap-1"
            >
              {showOriginal ? (
                <>
                  <EyeOff className="h-3 w-3" />
                  Show Scrambled
                </>
              ) : (
                <>
                  <Eye className="h-3 w-3" />
                  Show Original
                </>
              )}
            </Button>
          )}
        </div>
        
        <div className="flex items-center gap-1">
          <Button
            variant="outline"
            size="sm"
            onClick={() => handlePageChange(currentPage - 1)}
            disabled={currentPage <= 1}
          >
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => handlePageChange(currentPage + 1)}
            disabled={currentPage >= previewInfo.total_pages}
          >
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Image Preview */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Scrambled Image */}
        <Card className="p-4">
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-sm font-medium">
              <AlertTriangle className="h-4 w-4 text-destructive" />
              Scrambled Version
            </div>
            <div className="relative aspect-[3/4] bg-gradient-to-br from-red-50 to-red-100 rounded border-2 border-red-200 overflow-hidden">
              {imageLoading && (
                <div className="absolute inset-0 flex items-center justify-center bg-background/80">
                  <Loader2 className="h-6 w-6 animate-spin" />
                </div>
              )}
              <img
                src={`http://localhost:5000/api/preview/scrambled/${examId}/${currentPage}`}
                alt={`Scrambled page ${currentPage}`}
                className="w-full h-full object-contain"
                onLoad={handleImageLoad}
                onError={handleImageError}
                style={{ display: imageLoading ? 'none' : 'block' }}
              />
              <div className="absolute top-2 right-2">
                <Badge variant="destructive" className="text-xs">
                  <Shield className="h-3 w-3 mr-1" />
                  ENCRYPTED
                </Badge>
              </div>
            </div>
          </div>
        </Card>

        {/* Original Image */}
        <Card className="p-4">
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-sm font-medium">
              {keyReleased ? (
                <>
                  <CheckCircle className="h-4 w-4 text-green-600" />
                  Original Version
                </>
              ) : (
                <>
                  <Lock className="h-4 w-4 text-muted-foreground" />
                  Original (Locked)
                </>
              )}
            </div>
            <div className={`relative aspect-[3/4] rounded border-2 overflow-hidden transition-all duration-500 ${
              keyReleased && showOriginal
                ? 'bg-gradient-to-br from-green-50 to-green-100 border-green-200'
                : 'bg-muted border-muted-foreground/20'
            }`}>
              {keyReleased && showOriginal ? (
                <>
                  {imageLoading && (
                    <div className="absolute inset-0 flex items-center justify-center bg-background/80">
                      <Loader2 className="h-6 w-6 animate-spin" />
                    </div>
                  )}
                  <img
                    src={`http://localhost:5000/api/preview/original/${examId}/${currentPage}`}
                    alt={`Original page ${currentPage}`}
                    className="w-full h-full object-contain"
                    onLoad={handleImageLoad}
                    onError={handleImageError}
                    style={{ display: imageLoading ? 'none' : 'block' }}
                  />
                  <div className="absolute top-2 right-2">
                    <Badge variant="default" className="text-xs bg-green-600">
                      <FileText className="h-3 w-3 mr-1" />
                      READABLE
                    </Badge>
                  </div>
                </>
              ) : (
                <div className={`flex items-center justify-center h-full ${!keyReleased ? 'blur-sm' : ''}`}>
                  <div className="text-center p-4">
                    {keyReleased ? (
                      <>
                        <Eye className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
                        <p className="text-sm text-muted-foreground">Click "Show Original" to view</p>
                      </>
                    ) : (
                      <>
                        <Lock className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
                        <p className="text-sm text-muted-foreground">Awaiting key release</p>
                      </>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default ImagePreview;