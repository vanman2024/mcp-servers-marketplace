import React, { useState, useEffect } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';


// Validation schema
const validationSchema = yup.object({
        exercise: yup.required()
    sets: yup.number()
    reps: yup.number()
    weight: yup.number()
});


interface Workout_TrackerFormData {
        exercise: string;
    sets: number;
    reps: number;
    weight: number;
}

const Workout_TrackerForm: React.FC = () => {
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [submitMessage, setSubmitMessage] = useState<string>('');
    
    const {
        register,
        handleSubmit,
        formState: { errors, isValid },
        reset,
        watch
    } = useForm<Workout_TrackerFormData>({
        resolver: yupResolver(validationSchema),
        mode: 'onChange'
    });
    
    const onSubmit: SubmitHandler<Workout_TrackerFormData> = async (data) => {
        setIsSubmitting(true);
        setSubmitMessage('');
        
        try {
            
            // Handle form submission action: saveWorkout
            console.log('Form data:', data);
            
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            setSubmitMessage('Form submitted successfully!');
            reset();
            
        } catch (error) {
            setSubmitMessage('Error submitting form. Please try again.');
            console.error('Form submission error:', error);
        } finally {
            setIsSubmitting(false);
        }
    };
    
    return (
        <div className="max-w-md mx-auto bg-white shadow-lg rounded-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
                Workout Tracker
            </h2>
            
            
            
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                
                {/* Form fields based on validation schema */}
                
                <div>
                    <label htmlFor="exercise" className="block text-sm font-medium text-gray-700 mb-1">
                        Exercise
                    </label>
                    <input
                        id="exercise"
                        type="text"
                        {...register('exercise')}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Enter exercise"
                    />
                    {errors.exercise && (
                        <p className="mt-1 text-sm text-red-600">{errors.exercise?.message}</p>
                    )}
                </div>
                

                <div>
                    <label htmlFor="sets" className="block text-sm font-medium text-gray-700 mb-1">
                        Sets
                    </label>
                    <input
                        id="sets"
                        type="text"
                        {...register('sets')}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Enter sets"
                    />
                    {errors.sets && (
                        <p className="mt-1 text-sm text-red-600">{errors.sets?.message}</p>
                    )}
                </div>
                

                <div>
                    <label htmlFor="reps" className="block text-sm font-medium text-gray-700 mb-1">
                        Reps
                    </label>
                    <input
                        id="reps"
                        type="text"
                        {...register('reps')}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Enter reps"
                    />
                    {errors.reps && (
                        <p className="mt-1 text-sm text-red-600">{errors.reps?.message}</p>
                    )}
                </div>
                

                <div>
                    <label htmlFor="weight" className="block text-sm font-medium text-gray-700 mb-1">
                        Weight
                    </label>
                    <input
                        id="weight"
                        type="text"
                        {...register('weight')}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Enter weight"
                    />
                    {errors.weight && (
                        <p className="mt-1 text-sm text-red-600">{errors.weight?.message}</p>
                    )}
                </div>
                
                
                
                {/* Submit button */}
                <button
                    type="submit"
                    disabled={isSubmitting || !isValid}
                    className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {isSubmitting ? 'Submitting...' : 'Submit'}
                </button>
                
                {/* Submit message */}
                {submitMessage && (
                    <div className={`text-center text-sm ${submitMessage.includes('Error') ? 'text-red-600' : 'text-green-600'}`}>
                        {submitMessage}
                    </div>
                )}
            </form>
        </div>
    );
};

export default Workout_TrackerForm;
