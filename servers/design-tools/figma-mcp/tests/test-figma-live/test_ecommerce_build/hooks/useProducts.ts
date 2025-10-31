import { useState, useEffect } from 'react';

export interface Product {
  id: string;
  title: string;
  description?: string;
  status: string;
  createdAt: Date;
  updatedAt: Date;
}

export function useProducts() {
  const [items, setItems] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load items from localStorage on mount
  useEffect(() => {
    try {
      const saved = localStorage.getItem('products');
      if (saved) {
        setItems(JSON.parse(saved));
      }
    } catch (err) {
      console.error('Failed to load products:', err);
    }
  }, []);

  // Save to localStorage when items change
  useEffect(() => {
    try {
      localStorage.setItem('products', JSON.stringify(items));
    } catch (err) {
      console.error('Failed to save products:', err);
    }
  }, [items]);

  const addProduct = async (data: Partial<Product>) => {
    setLoading(true);
    setError(null);
    
    try {
      const newProduct: Product = {
        id: Date.now().toString(),
        title: data.title || '',
        description: data.description,
        status: data.status || 'active',
        createdAt: new Date(),
        updatedAt: new Date(),
        ...data
      };
      
      setItems(prev => [...prev, newProduct]);
      return newProduct;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to add product';
      setError(message);
      throw new Error(message);
    } finally {
      setLoading(false);
    }
  };

  const updateProduct = async (id: string, updates: Partial<Product>) => {
    setLoading(true);
    setError(null);
    
    try {
      setItems(prev => prev.map(item => 
        item.id === id 
          ? { ...item, ...updates, updatedAt: new Date() }
          : item
      ));
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to update product';
      setError(message);
      throw new Error(message);
    } finally {
      setLoading(false);
    }
  };

  const deleteProduct = async (id: string) => {
    setLoading(true);
    setError(null);
    
    try {
      setItems(prev => prev.filter(item => item.id !== id));
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to delete product';
      setError(message);
      throw new Error(message);
    } finally {
      setLoading(false);
    }
  };

  return {
    items,
    loading,
    error,
    addProduct,
    updateProduct,
    deleteProduct
  };
}