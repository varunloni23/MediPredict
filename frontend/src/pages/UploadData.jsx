import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

const UploadData = () => {
  const [selectedFile, setSelectedFile] = useState(null)
  const [deviceId, setDeviceId] = useState('')
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0])
    setError('')
  }

  const handleDeviceIdChange = (event) => {
    setDeviceId(event.target.value)
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    
    if (!selectedFile) {
      setError('Please select a file to upload')
      return
    }
    
    if (!deviceId) {
      setError('Please enter a device ID')
      return
    }
    
    setUploading(true)
    setMessage('')
    setError('')
    
    try {
      // Create FormData for file upload
      const formData = new FormData()
      formData.append('file', selectedFile)
      
      // Make API call to upload the file
      const response = await fetch(`http://localhost:8001/api/devices/${deviceId}/upload-data`, {
        method: 'POST',
        body: formData,
      })
      
      if (response.ok) {
        const result = await response.json()
        setMessage(result.message || 'File uploaded successfully!')
        setSelectedFile(null)
        setDeviceId('')
        
        // Redirect to devices page after successful upload
        setTimeout(() => {
          navigate('/devices')
        }, 2000)
      } else {
        const errorData = await response.json()
        setError(errorData.detail || 'Failed to upload file. Please try again.')
      }
    } catch (err) {
      console.error('Upload error:', err)
      setError('Failed to upload file. Please try again.')
    } finally {
      setUploading(false)
    }
  }

  // Handle manual data entry
  const handleManualEntry = () => {
    // For now, just navigate to devices page with a message
    // In a real app, this would open a modal or form for manual entry
    alert('Manual entry feature would open here. For now, you can upload a CSV file.')
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Upload Device Data</h1>
      
      <div className="bg-white shadow sm:rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h2 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Upload CSV or Excel file
          </h2>
          
          {error && (
            <div className="rounded-md bg-red-50 p-4 mb-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">
                    {error}
                  </h3>
                </div>
              </div>
            </div>
          )}
          
          {message && (
            <div className="rounded-md bg-green-50 p-4 mb-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-green-800">
                    {message}
                  </p>
                </div>
              </div>
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="deviceId" className="block text-sm font-medium text-gray-700">
                Device ID
              </label>
              <input
                type="text"
                id="deviceId"
                value={deviceId}
                onChange={handleDeviceIdChange}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Enter device ID"
              />
            </div>
            
            <div>
              <label htmlFor="file-upload" className="block text-sm font-medium text-gray-700">
                Upload File
              </label>
              <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                <div className="space-y-1 text-center">
                  <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                    <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                  <div className="flex text-sm text-gray-600">
                    <label htmlFor="file-upload" className="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500">
                      <span>Upload a file</span>
                      <input
                        id="file-upload"
                        name="file-upload"
                        type="file"
                        className="sr-only"
                        onChange={handleFileChange}
                        accept=".csv,.xlsx,.xls"
                      />
                    </label>
                    <p className="pl-1">or drag and drop</p>
                  </div>
                  <p className="text-xs text-gray-500">
                    CSV, XLSX, or XLS up to 10MB
                  </p>
                </div>
              </div>
              {selectedFile && (
                <p className="mt-2 text-sm text-gray-500">
                  Selected file: {selectedFile.name}
                </p>
              )}
            </div>
            
            <div>
              <button
                type="submit"
                disabled={uploading}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
              >
                {uploading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Uploading...
                  </>
                ) : (
                  'Upload Data'
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
      
      <div className="mt-8 bg-white shadow sm:rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h2 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Manual Data Entry
          </h2>
          <p className="text-sm text-gray-500 mb-4">
            Enter device data manually if you don't have a file to upload.
          </p>
          <button
            type="button"
            onClick={handleManualEntry}
            className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Add Manual Entry
          </button>
        </div>
      </div>
    </div>
  )
}

export default UploadData