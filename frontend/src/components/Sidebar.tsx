import React, { useState, useEffect } from 'react'; // Added useEffect
import { Drawer, Toolbar, Box, TextField, Button, RadioGroup, FormControlLabel, Radio, FormControl, FormLabel, Select, MenuItem, InputLabel, CircularProgress } from '@mui/material'; // Added Select, MenuItem, InputLabel, CircularProgress
import PositiveIcon from '@mui/icons-material/SentimentSatisfiedAlt';
import NegativeIcon from '@mui/icons-material/SentimentDissatisfied';
import { getPersonaSegments, PersonaSegmentsResponse } from '../services/api'; // Added import for API service

interface SidebarProps {
  onGenerate: (product: string, productDescription: string, selectedPersonaProfile?: string) => void; // Removed customerType
  drawerWidth?: number;
  availablePersonaProfiles: string[];
  isLoadingPersonas: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({ onGenerate, drawerWidth = 240, availablePersonaProfiles, isLoadingPersonas }) => {
  const [product, setProduct] = useState<string>('');
  const [productDescription, setProductDescription] = useState<string>('');
  // const [selectedCustomerType, setSelectedCustomerType] = useState<'positive' | 'negative' | null>(null); // Removed
  const [selectedPersonaProfile, setSelectedPersonaProfile] = useState<string>('');

  // Effect to update selectedPersonaProfile when availablePersonaProfiles changes (e.g., on initial load)
  useEffect(() => {
    if (availablePersonaProfiles && availablePersonaProfiles.length > 0) {
      // If no profile is selected yet, or if the current selection is no longer valid, select the first one.
      if (!selectedPersonaProfile || !availablePersonaProfiles.includes(selectedPersonaProfile)) {
        setSelectedPersonaProfile(availablePersonaProfiles[0]);
      }
    } else {
      setSelectedPersonaProfile(''); // Clear selection if no profiles are available
    }
  }, [availablePersonaProfiles, selectedPersonaProfile]); // Rerun when availablePersonaProfiles or selectedPersonaProfile changes

  const handleSubmit = () => {
    // Removed customer type check
    if (!selectedPersonaProfile) { // Ensure a persona is selected
        alert('Please select a Persona Segment.');
        return;
    }
    if (!product.trim()) {
      alert('Please enter a product name.');
      return;
    }
    if (!productDescription.trim()) {
      alert('Please enter a product description.');
      return;
    }
    onGenerate(product, productDescription, selectedPersonaProfile); // Pass selectedPersonaProfile
  };

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
      }}
    >
      <Toolbar /> {/* For spacing below the AppBar if you add one later */}
      <Box sx={{ overflow: 'auto', p: 2 }}> {/* Added padding to Box */}
        {isLoadingPersonas ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', mb: 2 }}>
            <CircularProgress size={24} />
            <span style={{ marginLeft: '8px' }}>Loading Personas...</span>
          </Box>
        ) : availablePersonaProfiles.length > 0 ? (
          <FormControl fullWidth sx={{ mb: 2 }} disabled={isLoadingPersonas}>
            <InputLabel id="persona-profile-select-label">Persona Segment</InputLabel>
            <Select
              labelId="persona-profile-select-label"
              id="persona-profile-select"
              value={selectedPersonaProfile}
              label="Persona Segment"
              onChange={(e) => setSelectedPersonaProfile(e.target.value as string)}
            >
              {availablePersonaProfiles.map((profile) => (
                <MenuItem key={profile} value={profile}>
                  {profile.replace(/_/g, ' ')} {/* Format profile string for display */}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        ) : (
          <Box sx={{ mb: 2, color: 'text.secondary' }}>No persona segments available or failed to load.</Box>
        )}

        {/* Removed Customer Type FormControl and RadioGroup */}
        
        <TextField
          label="Product Name"
          variant="outlined"
          fullWidth
          value={product}
          onChange={(e) => setProduct(e.target.value)}
          sx={{ mt: 2, mb: 1 }} 
        />
        <TextField
          label="Product Description"
          variant="outlined"
          fullWidth
          multiline
          rows={3}
          value={productDescription}
          onChange={(e) => setProductDescription(e.target.value)}
          sx={{ mb: 2 }}
        />
        <Button 
          variant="contained" 
          color="primary" 
          onClick={handleSubmit}
          fullWidth
        >
          Submit
        </Button>
      </Box>
    </Drawer>
  );
};

export default Sidebar;
