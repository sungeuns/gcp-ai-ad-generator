import React, { useState } from 'react';
import { Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Toolbar, Box, TextField, Button, RadioGroup, FormControlLabel, Radio, FormControl, FormLabel } from '@mui/material';
import PositiveIcon from '@mui/icons-material/SentimentSatisfiedAlt'; // Example icon
import NegativeIcon from '@mui/icons-material/SentimentDissatisfied'; // Example icon

interface SidebarProps {
  onGenerate: (customerType: 'positive' | 'negative', product: string, productDescription: string) => void;
  drawerWidth?: number;
}

const Sidebar: React.FC<SidebarProps> = ({ onGenerate, drawerWidth = 240 }) => {
  const [product, setProduct] = useState<string>('');
  const [productDescription, setProductDescription] = useState<string>('');
  const [selectedCustomerType, setSelectedCustomerType] = useState<'positive' | 'negative' | null>(null);

  const handleSubmit = () => {
    if (!selectedCustomerType) {
      alert('Please select a customer type (Positive or Negative).');
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
    onGenerate(selectedCustomerType, product, productDescription);
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
        <FormControl component="fieldset" sx={{ mb: 2 }}>
          <FormLabel component="legend">Customer Type</FormLabel>
          <RadioGroup
            aria-label="customer-type"
            name="customer-type-radio-buttons-group"
            value={selectedCustomerType}
            onChange={(e) => setSelectedCustomerType(e.target.value as 'positive' | 'negative')}
          >
            <FormControlLabel 
              value="positive" 
              control={<Radio />} 
              label={<Box sx={{ display: 'flex', alignItems: 'center' }}><PositiveIcon color="success" sx={{ mr: 1 }} /> Positive</Box>} 
            />
            <FormControlLabel 
              value="negative" 
              control={<Radio />} 
              label={<Box sx={{ display: 'flex', alignItems: 'center' }}><NegativeIcon color="error" sx={{ mr: 1 }} /> Negative</Box>}
            />
          </RadioGroup>
        </FormControl>
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
