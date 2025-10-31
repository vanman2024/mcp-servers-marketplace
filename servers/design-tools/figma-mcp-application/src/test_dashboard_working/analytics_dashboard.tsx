import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';

const AnalyticsDashboard = () => {
    const router = useRouter();
    const [refreshInterval, setRefreshInterval] = useState(null);
    
    // Auto-refresh effect
    useEffect(() => {
        if (refreshInterval) {
            const interval = setInterval(() => {
                // Refresh dashboard data
                console.log('Refreshing dashboard data...');
            }, refreshInterval * 1000);
            
            return () => clearInterval(interval);
        }
    }, [refreshInterval]);
    
    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            
<div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Sidebar -->
    <div class="fixed inset-y-0 left-0 z-50 w-64 bg-white dark:bg-gray-800 shadow-lg transform transition-transform duration-300"
         style="width: 16rem">
        <div class="flex h-full flex-col">
            <!-- Logo -->
            <div class="flex h-16 items-center justify-center border-b border-gray-200 dark:border-gray-700">
                <h1 class="text-xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
            </div>
            
            <!-- Navigation -->
            <nav class="flex-1 space-y-1 px-2 py-4">
                
                <a href="/dashboard" class="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
                    <svg class="mr-3 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
                    </svg>
                    Overview
                </a>
                 
                <a href="/dashboard/analytics" class="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
                    <svg class="mr-3 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
                    </svg>
                    Analytics
                </a>
                 
                <a href="/dashboard/users" class="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
                    <svg class="mr-3 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
                    </svg>
                    Users
                </a>
                 
                <a href="/dashboard/settings" class="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
                    <svg class="mr-3 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
                    </svg>
                    Settings
                </a>
                
            </nav>
            
            <!-- User menu -->
            <div class="border-t border-gray-200 dark:border-gray-700 p-4">
                <div class="flex items-center">
                    <img class="h-8 w-8 rounded-full" src="/api/placeholder/32/32" alt="User">
                    <div class="ml-3">
                        <p class="text-sm font-medium text-gray-700 dark:text-gray-300">User Name</p>
                        <p class="text-xs text-gray-500 dark:text-gray-400">View profile</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Main content -->
    <div class="pl-64" style="padding-left: 16rem">
        <!-- Top bar -->
        <header class="bg-white dark:bg-gray-800 shadow">
            <div class="px-4 sm:px-6 lg:px-8">
                <div class="flex h-16 items-center justify-between">
                    <h2 class="text-xl font-semibold text-gray-900 dark:text-white">
                        Analytics Dashboard
                    </h2>
                    
                    <!-- Actions -->
                    <div class="flex items-center space-x-4">
                        <button class="p-2 text-gray-400 hover:text-gray-500">
                            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                            </svg>
                        </button>
                        <button class="p-2 text-gray-400 hover:text-gray-500">
                            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        </header>
        
        <!-- Dashboard content -->
        <main class="p-6">
            <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                <!-- Widgets will be inserted here -->
            </div>
        </main>
    </div>
</div>
            
        </div>
    );
};

export default AnalyticsDashboard;
