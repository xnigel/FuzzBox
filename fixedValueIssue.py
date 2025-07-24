def validate_hex_input(self, P, field_idx):
    # Allow empty string for deletion
    if P == "":
        self.field_lengths[field_idx].config(state=tk.NORMAL) # Enable length entry
        self.field_lengths[field_idx].delete(0, tk.END)
        self.field_lengths[field_idx].insert(0, "")
        self.field_lengths[field_idx].config(state=tk.DISABLED) # Disable it again
        return True
        
    # Check if it's a valid hex string
    if not all(c in '0123456789abcdefABCDEF' for c in P):
        return False
        
    # Update length based on hex string
    byte_length = len(P) // 2
    self.field_lengths[field_idx].config(state=tk.NORMAL) # Temporarily enable to update
    self.field_lengths[field_idx].delete(0, tk.END)
    self.field_lengths[field_idx].insert(0, str(byte_length))
    self.field_lengths[field_idx].config(state=tk.DISABLED) # Disable it again
    return True