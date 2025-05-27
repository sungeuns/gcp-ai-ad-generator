import React, { useState } from 'react';
import './App.css';
import { Box, CssBaseline, Typography, Alert, Snackbar } from '@mui/material';
import Sidebar from './components/Sidebar';
import AdDisplay from './components/AdDisplay';
import { generateAdContent, AdGenerationRequestPayload, AdGenerationResponseData } from './services/api';

interface AdVariation {
  adText: string | null;
  adImageData: string | null;
}

const initialAdVariations: AdVariation[] = [
  { adText: null, adImageData: null },
  { adText: null, adImageData: null },
  { adText: null, adImageData: null },
];

function App() {
  const [adVariations, setAdVariations] = useState<AdVariation[]>(initialAdVariations);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateAd = async (customerType: 'positive' | 'negative', product: string, productDescription: string) => {
    setIsLoading(true);
    setError(null);
    setAdVariations(initialAdVariations); // Reset to initial state

    try {
      const payload: AdGenerationRequestPayload = {
        customer_type: customerType,
        product: product,
        product_description: productDescription,
        number_of_variations: 3 // Request 3 variations from the backend
      };

      // Call the API once to get all three variations
      const response = await generateAdContent(payload);
      
      if (response.creatives && response.creatives.length > 0) {
        const newAdVariations: AdVariation[] = response.creatives.map(creative => ({
          adText: creative.ad_text,
          adImageData: creative.ad_image_data
        }));
        // Ensure we always have 3 variations for display, padding with nulls if fewer are returned
        const paddedVariations = [...newAdVariations];
        while (paddedVariations.length < 3) {
          paddedVariations.push({ adText: null, adImageData: null });
        }
        setAdVariations(paddedVariations.slice(0, 3)); // Take up to 3
      } else {
        // Handle cases where no creatives are returned or the array is empty
        console.error("No creatives returned from API or creatives array is empty.");
        setError('Failed to generate ad variations: No creatives received.');
        setAdVariations(initialAdVariations); // Reset to empty state
      }

    } catch (err: any) {
      console.error("Failed to generate ad variations:", err);
      setError(err.message || 'An unexpected error occurred while generating ad variations.');
      // Optionally, set adVariations to a state indicating error for all, or handle per-ad errors if Promise.allSettled was used
    } finally {
      setIsLoading(false);
    }
  };

  const handleCloseSnackbar = () => {
    setError(null);
  };

  const drawerWidth = 240;

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline /> {/* Ensures consistent baseline styling */}
      <Sidebar onGenerate={handleGenerateAd} drawerWidth={drawerWidth} />
      <Box
        component="main"
        sx={{ 
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          display: 'flex',
          flexDirection: 'column', // Main axis for title and ad container
          alignItems: 'center', // Center title
          // justifyContent: 'center', // Removed to allow ad container to take space
          minHeight: '100vh'
        }}
      >
        <Typography variant="h4" component="h1" gutterBottom sx={{ textAlign: 'center', mb: 3 }}>
          AI Ad Generator
        </Typography>
        <Box 
          sx={{
            display: 'flex',
            flexDirection: 'row',
            justifyContent: 'space-around',
            alignItems: 'flex-start', // Ads might have different heights
            flexWrap: 'wrap', // Allow wrapping on smaller screens
            gap: 2, // Spacing between ad displays
            width: '100%', // Take full width of the main content area
            mt: 2 // Margin top
          }}
        >
          {adVariations.map((ad, index) => (
            <AdDisplay
              key={index}
              adText={ad.adText}
              adImageData={ad.adImageData}
              isLoading={isLoading} // Pass global loading state; AdDisplay handles its internal view
            />
          ))}
        </Box>
      </Box>

      {error && (
        <Snackbar 
          open={!!error} 
          autoHideDuration={6000} 
          onClose={handleCloseSnackbar}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        >
          <Alert onClose={handleCloseSnackbar} severity="error" sx={{ width: '100%' }}>
            {error}
          </Alert>
        </Snackbar>
      )}
    </Box>
  );
}

export default App;
