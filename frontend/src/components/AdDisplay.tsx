import React from 'react';
import { Paper, Typography, Box, Card, CardMedia, CardContent, CircularProgress } from '@mui/material';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface AdDisplayProps {
  adText: string | null;
  adImageData: string | null; // Changed prop name
  isLoading: boolean;
}

const AdDisplay: React.FC<AdDisplayProps> = ({ adText, adImageData, isLoading }) => {
  // Check if adImageData looks like a valid data URI
  const isValidDataUri = adImageData && adImageData.startsWith('data:image');

  // console.log("Is valid data uri : " + isValidDataUri);

  return (
    <Paper 
      elevation={3} 
      sx={{ 
        width: 400, // Typical smartphone width (approx)
        height: 800, // Typical smartphone height (approx)
        p: 2, 
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center', 
        justifyContent: 'center',
        overflow: 'hidden', // To mimic phone screen boundaries
        bgcolor: 'background.default', // Or a specific phone background color
        borderRadius: '26px', // Rounded corners for phone look
        border: '10px solid black', // Phone bezel
        boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
        position: 'relative', // For absolute positioning of loader
      }}
    >
      {isLoading && (
        <Box 
          sx={{ 
            position: 'absolute', 
            top: 0, 
            left: 0, 
            right: 0, 
            bottom: 0, 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            backgroundColor: 'rgba(255, 255, 255, 0.7)', // Semi-transparent overlay
            zIndex: 10 
          }}
        >
          <CircularProgress size={78} />
        </Box>
      )}
      
      {!isLoading && !adText && !adImageData && ( // Changed to adImageData
        <Typography variant="h6" color="text.secondary" textAlign="center">
          Click a button on the left to generate an ad!
        </Typography>
      )}

      {!isLoading && (adText || adImageData) && ( // Changed to adImageData
        <Card sx={{ width: '100%', height: '100%', boxShadow: 'none', bgcolor: 'transparent' }}>
          {isValidDataUri ? (
            <CardMedia
              component="img"
              alt="Generated Ad Image"
              image={adImageData} // Use adImageData
              sx={{ 
                maxHeight: '60%', 
                width: '100%', 
                objectFit: 'contain', 
                mb: 1, 
              }}
            />
          ) : adImageData ? ( // If adImageData exists but is not a valid data URI (e.g., an error message from backend)
            <Typography variant="caption" color="error" textAlign="center" sx={{ p:2, wordBreak: 'break-all' }}>
              Could not display image. Received: {adImageData}
            </Typography>
          ) : null}
          <CardContent sx={{ flexGrow: 1, overflowY: 'auto', p: 1, textAlign: 'left', width: '100%' }}>
            {adText && (
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {adText}
              </ReactMarkdown>
            )}
          </CardContent>
        </Card>
      )}
    </Paper>
  );
};

export default AdDisplay;
