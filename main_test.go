package main

import (
	"errors"
	"testing"
	"time"
)

// TestSpiderConfig tests the SpiderConfig functionality
func TestSpiderConfig(t *testing.T) {
	t.Run("NewSpiderConfig", func(t *testing.T) {
		config := NewSpiderConfig()
		if config == nil {
			t.Fatal("NewSpiderConfig returned nil")
		}
		if config.MaxDepth != DefaultMaxDepth {
			t.Errorf("Expected MaxDepth %d, got %d", DefaultMaxDepth, config.MaxDepth)
		}
		if config.MaxPages != DefaultMaxPages {
			t.Errorf("Expected MaxPages %d, got %d", DefaultMaxPages, config.MaxPages)
		}
		if config.Delay != DefaultDelay {
			t.Errorf("Expected Delay %v, got %v", DefaultDelay, config.Delay)
		}
		if config.UserAgent != DefaultUserAgent {
			t.Errorf("Expected UserAgent %s, got %s", DefaultUserAgent, config.UserAgent)
		}
		if config.Timeout != DefaultTimeout {
			t.Errorf("Expected Timeout %v, got %v", DefaultTimeout, config.Timeout)
		}
		if config.Concurrency != DefaultConcurrency {
			t.Errorf("Expected Concurrency %d, got %d", DefaultConcurrency, config.Concurrency)
		}
	})

	t.Run("SetMaxDepth", func(t *testing.T) {
		config := NewSpiderConfig()
		
		// Test valid depth
		err := config.SetMaxDepth(5)
		if err != nil {
			t.Errorf("Unexpected error: %v", err)
		}
		if config.MaxDepth != 5 {
			t.Errorf("Expected MaxDepth 5, got %d", config.MaxDepth)
		}
		
		// Test negative depth
		err = config.SetMaxDepth(-1)
		if err == nil {
			t.Error("Expected error for negative depth")
		}
		if config.MaxDepth != 5 { // Should remain unchanged
			t.Errorf("Expected MaxDepth to remain 5, got %d", config.MaxDepth)
		}
	})

	t.Run("SetMaxPages", func(t *testing.T) {
		config := NewSpiderConfig()
		
		// Test valid pages
		err := config.SetMaxPages(200)
		if err != nil {
			t.Errorf("Unexpected error: %v", err)
		}
		if config.MaxPages != 200 {
			t.Errorf("Expected MaxPages 200, got %d", config.MaxPages)
		}
		
		// Test negative pages
		err = config.SetMaxPages(-1)
		if err == nil {
			t.Error("Expected error for negative pages")
		}
	})

	t.Run("SetDelay", func(t *testing.T) {
		config := NewSpiderConfig()
		
		// Test valid delay
		delay := 2 * time.Second
		err := config.SetDelay(delay)
		if err != nil {
			t.Errorf("Unexpected error: %v", err)
		}
		if config.Delay != delay {
			t.Errorf("Expected Delay %v, got %v", delay, config.Delay)
		}
		
		// Test negative delay
		err = config.SetDelay(-1 * time.Second)
		if err == nil {
			t.Error("Expected error for negative delay")
		}
	})

	t.Run("SetUserAgent", func(t *testing.T) {
		config := NewSpiderConfig()
		
		// Test valid user agent
		ua := "TestBot/1.0"
		err := config.SetUserAgent(ua)
		if err != nil {
			t.Errorf("Unexpected error: %v", err)
		}
		if config.UserAgent != ua {
			t.Errorf("Expected UserAgent %s, got %s", ua, config.UserAgent)
		}
		
		// Test empty user agent
		err = config.SetUserAgent("")
		if err == nil {
			t.Error("Expected error for empty user agent")
		}
	})

	t.Run("SetTimeout", func(t *testing.T) {
		config := NewSpiderConfig()
		
		// Test valid timeout
		timeout := 60 * time.Second
		err := config.SetTimeout(timeout)
		if err != nil {
			t.Errorf("Unexpected error: %v", err)
		}
		if config.Timeout != timeout {
			t.Errorf("Expected Timeout %v, got %v", timeout, config.Timeout)
		}
		
		// Test zero timeout
		err = config.SetTimeout(0)
		if err == nil {
			t.Error("Expected error for zero timeout")
		}
		
		// Test negative timeout
		err = config.SetTimeout(-1 * time.Second)
		if err == nil {
			t.Error("Expected error for negative timeout")
		}
	})

	t.Run("SetConcurrency", func(t *testing.T) {
		config := NewSpiderConfig()
		
		// Test valid concurrency
		err := config.SetConcurrency(10)
		if err != nil {
			t.Errorf("Unexpected error: %v", err)
		}
		if config.Concurrency != 10 {
			t.Errorf("Expected Concurrency 10, got %d", config.Concurrency)
		}
		
		// Test zero concurrency
		err = config.SetConcurrency(0)
		if err == nil {
			t.Error("Expected error for zero concurrency")
		}
		
		// Test negative concurrency
		err = config.SetConcurrency(-1)
		if err == nil {
			t.Error("Expected error for negative concurrency")
		}
	})

	t.Run("Validate", func(t *testing.T) {
		config := NewSpiderConfig()
		
		// Test valid config
		err := config.Validate()
		if err != nil {
			t.Errorf("Unexpected error for valid config: %v", err)
		}
		
		// Test invalid max depth
		config.MaxDepth = -1
		err = config.Validate()
		if err == nil {
			t.Error("Expected error for invalid max depth")
		}
		
		// Test invalid max pages
		config = NewSpiderConfig()
		config.MaxPages = -1
		err = config.Validate()
		if err == nil {
			t.Error("Expected error for invalid max pages")
		}
		
		// Test invalid delay
		config = NewSpiderConfig()
		config.Delay = -1 * time.Second
		err = config.Validate()
		if err == nil {
			t.Error("Expected error for invalid delay")
		}
		
		// Test empty user agent
		config = NewSpiderConfig()
		config.UserAgent = ""
		err = config.Validate()
		if err == nil {
			t.Error("Expected error for empty user agent")
		}
		
		// Test invalid timeout
		config = NewSpiderConfig()
		config.Timeout = 0
		err = config.Validate()
		if err == nil {
			t.Error("Expected error for invalid timeout")
		}
		
		// Test invalid concurrency
		config = NewSpiderConfig()
		config.Concurrency = 0
		err = config.Validate()
		if err == nil {
			t.Error("Expected error for invalid concurrency")
		}
	})
}

// TestSpider tests the Spider functionality
func TestSpider(t *testing.T) {
	t.Run("NewSpider", func(t *testing.T) {
		// Test with valid config
		config := NewSpiderConfig()
		spider, err := NewSpider(config)
		if err != nil {
			t.Errorf("Unexpected error: %v", err)
		}
		if spider == nil {
			t.Fatal("NewSpider returned nil")
		}
		if spider.config != config {
			t.Error("Spider config not set correctly")
		}
		if spider.client == nil {
			t.Error("Spider client not initialized")
		}
		if spider.logger == nil {
			t.Error("Spider logger not initialized")
		}
		
		// Test with nil config
		spider, err = NewSpider(nil)
		if err == nil {
			t.Error("Expected error for nil config")
		}
		if spider != nil {
			t.Error("Expected nil spider for nil config")
		}
		
		// Test with invalid config
		invalidConfig := NewSpiderConfig()
		invalidConfig.MaxDepth = -1
		spider, err = NewSpider(invalidConfig)
		if err == nil {
			t.Error("Expected error for invalid config")
		}
		if spider != nil {
			t.Error("Expected nil spider for invalid config")
		}
	})

	t.Run("Crawl", func(t *testing.T) {
		config := NewSpiderConfig()
		config.MaxPages = 2 // Limit for testing
		spider, err := NewSpider(config)
		if err != nil {
			t.Fatalf("Failed to create spider: %v", err)
		}
		
		// Test valid URL
		err = spider.Crawl("https://example.com")
		if err != nil {
			t.Errorf("Unexpected error: %v", err)
		}
		
		// Test empty URL
		err = spider.Crawl("")
		if err == nil {
			t.Error("Expected error for empty URL")
		}
	})

	t.Run("CrawlWithCallback", func(t *testing.T) {
		config := NewSpiderConfig()
		config.MaxPages = 2 // Limit for testing
		spider, err := NewSpider(config)
		if err != nil {
			t.Fatalf("Failed to create spider: %v", err)
		}
		
		// Test with valid callback
		callCount := 0
		callback := func(url string, err error) {
			callCount++
		}
		
		err = spider.CrawlWithCallback("https://example.com", callback)
		if err != nil {
			t.Errorf("Unexpected error: %v", err)
		}
		if callCount != config.MaxPages {
			t.Errorf("Expected %d callback calls, got %d", config.MaxPages, callCount)
		}
		
		// Test with empty URL
		err = spider.CrawlWithCallback("", callback)
		if err == nil {
			t.Error("Expected error for empty URL")
		}
		
		// Test with nil callback
		err = spider.CrawlWithCallback("https://example.com", nil)
		if err == nil {
			t.Error("Expected error for nil callback")
		}
	})

	t.Run("GetStats", func(t *testing.T) {
		config := NewSpiderConfig()
		spider, err := NewSpider(config)
		if err != nil {
			t.Fatalf("Failed to create spider: %v", err)
		}
		
		stats := spider.GetStats()
		if stats == nil {
			t.Fatal("GetStats returned nil")
		}
		
		expectedKeys := []string{"max_depth", "max_pages", "delay", "user_agent", "timeout", "concurrency"}
		for _, key := range expectedKeys {
			if _, exists := stats[key]; !exists {
				t.Errorf("Stats missing key: %s", key)
			}
		}
	})

	t.Run("Close", func(t *testing.T) {
		config := NewSpiderConfig()
		spider, err := NewSpider(config)
		if err != nil {
			t.Fatalf("Failed to create spider: %v", err)
		}
		
		err = spider.Close()
		if err != nil {
			t.Errorf("Unexpected error: %v", err)
		}
	})
}

// TestUtilityFunctions tests utility functions
func TestUtilityFunctions(t *testing.T) {
	t.Run("IsValidURL", func(t *testing.T) {
		// Test valid URLs
		validURLs := []string{
			"http://example.com",
			"https://example.com",
			"http://subdomain.example.com",
			"https://example.com/path",
		}
		
		for _, url := range validURLs {
			if !IsValidURL(url) {
				t.Errorf("Expected %s to be valid", url)
			}
		}
		
		// Test invalid URLs
		invalidURLs := []string{
			"",
			"ftp://example.com",
			"example.com",
			"http://",
			"https://",
		}
		
		for _, url := range invalidURLs {
			if IsValidURL(url) {
				t.Errorf("Expected %s to be invalid", url)
			}
		}
	})

	t.Run("ExtractDomain", func(t *testing.T) {
		// Test valid URLs
		testCases := []struct {
			url    string
			domain string
		}{
			{"http://example.com", "example.com"},
			{"https://example.com", "example.com"},
			{"http://subdomain.example.com", "subdomain.example.com"},
			{"https://example.com/path", "example.com"},
			{"http://example.com:8080", "example.com:8080"},
		}
		
		for _, tc := range testCases {
			domain, err := ExtractDomain(tc.url)
			if err != nil {
				t.Errorf("Unexpected error for %s: %v", tc.url, err)
			}
			if domain != tc.domain {
				t.Errorf("Expected domain %s for %s, got %s", tc.domain, tc.url, domain)
			}
		}
		
		// Test invalid URL
		_, err := ExtractDomain("invalid-url")
		if err == nil {
			t.Error("Expected error for invalid URL")
		}
	})

	t.Run("ParseDelay", func(t *testing.T) {
		// Test valid duration strings
		testCases := []struct {
			input    string
			expected time.Duration
		}{
			{"1s", time.Second},
			{"2m", 2 * time.Minute},
			{"500ms", 500 * time.Millisecond},
			{"5", 5 * time.Second},
			{"0", 0},
		}
		
		for _, tc := range testCases {
			duration, err := ParseDelay(tc.input)
			if err != nil {
				t.Errorf("Unexpected error for %s: %v", tc.input, err)
			}
			if duration != tc.expected {
				t.Errorf("Expected %v for %s, got %v", tc.expected, tc.input, duration)
			}
		}
		
		// Test invalid inputs
		invalidInputs := []string{"", "invalid", "-1s", "-5"}
		for _, input := range invalidInputs {
			_, err := ParseDelay(input)
			if err == nil {
				t.Errorf("Expected error for %s", input)
			}
		}
	})

	t.Run("ProcessURL", func(t *testing.T) {
		// Test valid URL
		url := "https://example.com"
		result, err := ProcessURL(url)
		if err != nil {
			t.Errorf("Unexpected error: %v", err)
		}
		if result == nil {
			t.Fatal("ProcessURL returned nil result")
		}
		if result["url"] != url {
			t.Errorf("Expected URL %s, got %s", url, result["url"])
		}
		if result["valid"] != true {
			t.Error("Expected valid to be true")
		}
		
		// Test invalid URL
		_, err = ProcessURL("invalid-url")
		if err == nil {
			t.Error("Expected error for invalid URL")
		}
	})

	t.Run("BatchProcessURLs", func(t *testing.T) {
		// Test valid URLs
		urls := []string{"https://example.com", "https://google.com"}
		results, err := BatchProcessURLs(urls)
		if err != nil {
			t.Errorf("Unexpected error: %v", err)
		}
		if len(results) != len(urls) {
			t.Errorf("Expected %d results, got %d", len(urls), len(results))
		}
		
		// Test empty URLs
		_, err = BatchProcessURLs([]string{})
		if err == nil {
			t.Error("Expected error for empty URLs")
		}
		
		// Test with invalid URL
		invalidURLs := []string{"https://example.com", "invalid-url"}
		_, err = BatchProcessURLs(invalidURLs)
		if err == nil {
			t.Error("Expected error for invalid URL in batch")
		}
	})
}

// TestErrorTypes tests error types
func TestErrorTypes(t *testing.T) {
	t.Run("SpiderError", func(t *testing.T) {
		errorType := "NetworkError"
		message := "Connection failed"
		url := "https://example.com"
		
		err := NewSpiderError(errorType, message, url)
		if err == nil {
			t.Fatal("NewSpiderError returned nil")
		}
		
		if err.Type != errorType {
			t.Errorf("Expected Type %s, got %s", errorType, err.Type)
		}
		if err.Message != message {
			t.Errorf("Expected Message %s, got %s", message, err.Message)
		}
		if err.URL != url {
			t.Errorf("Expected URL %s, got %s", url, err.URL)
		}
		
		// Test Error() method
		errorString := err.Error()
		expected := "NetworkError: Connection failed (URL: https://example.com)"
		if errorString != expected {
			t.Errorf("Expected error string %s, got %s", expected, errorString)
		}
	})
}

// TestVersionInfo tests version information
func TestVersionInfo(t *testing.T) {
	t.Run("GetVersion", func(t *testing.T) {
		version := GetVersion()
		if version == nil {
			t.Fatal("GetVersion returned nil")
		}
		
		expectedKeys := []string{"version", "build_time", "git_commit"}
		for _, key := range expectedKeys {
			if _, exists := version[key]; !exists {
				t.Errorf("Version missing key: %s", key)
			}
		}
		
		if version["version"] != Version {
			t.Errorf("Expected version %s, got %s", Version, version["version"])
		}
	})
}

// TestConstants tests constants
func TestConstants(t *testing.T) {
	if DefaultMaxDepth != 3 {
		t.Errorf("Expected DefaultMaxDepth 3, got %d", DefaultMaxDepth)
	}
	if DefaultMaxPages != 100 {
		t.Errorf("Expected DefaultMaxPages 100, got %d", DefaultMaxPages)
	}
	if DefaultDelay != time.Second {
		t.Errorf("Expected DefaultDelay %v, got %v", time.Second, DefaultDelay)
	}
	if DefaultUserAgent != "DirectWebSpider/1.0" {
		t.Errorf("Expected DefaultUserAgent %s, got %s", "DirectWebSpider/1.0", DefaultUserAgent)
	}
	if DefaultTimeout != 30*time.Second {
		t.Errorf("Expected DefaultTimeout %v, got %v", 30*time.Second, DefaultTimeout)
	}
	if DefaultConcurrency != 5 {
		t.Errorf("Expected DefaultConcurrency 5, got %d", DefaultConcurrency)
	}
}

// Benchmark tests
func BenchmarkSpiderConfigCreation(b *testing.B) {
	for i := 0; i < b.N; i++ {
		_ = NewSpiderConfig()
	}
}

func BenchmarkSpiderCreation(b *testing.B) {
	config := NewSpiderConfig()
	for i := 0; i < b.N; i++ {
		spider, _ := NewSpider(config)
		if spider != nil {
			spider.Close()
		}
	}
}

func BenchmarkIsValidURL(b *testing.B) {
	url := "https://example.com"
	for i := 0; i < b.N; i++ {
		_ = IsValidURL(url)
	}
}

func BenchmarkExtractDomain(b *testing.B) {
	url := "https://example.com/path"
	for i := 0; i < b.N; i++ {
		_, _ = ExtractDomain(url)
	}
}

func BenchmarkProcessURL(b *testing.B) {
	url := "https://example.com"
	for i := 0; i < b.N; i++ {
		_, _ = ProcessURL(url)
	}
}

// Test edge cases and error conditions
func TestEdgeCases(t *testing.T) {
	t.Run("SpiderConfigEdgeCases", func(t *testing.T) {
		config := NewSpiderConfig()
		
		// Test boundary values
		err := config.SetMaxDepth(0)
		if err != nil {
			t.Errorf("Unexpected error for MaxDepth 0: %v", err)
		}
		
		err = config.SetMaxPages(0)
		if err != nil {
			t.Errorf("Unexpected error for MaxPages 0: %v", err)
		}
		
		err = config.SetDelay(0)
		if err != nil {
			t.Errorf("Unexpected error for Delay 0: %v", err)
		}
		
		err = config.SetConcurrency(1)
		if err != nil {
			t.Errorf("Unexpected error for Concurrency 1: %v", err)
		}
	})

	t.Run("URLProcessingEdgeCases", func(t *testing.T) {
		// Test URLs with special characters
		specialURLs := []string{
			"https://example.com/path?param=value&other=test",
			"https://example.com:8080/path",
			"https://sub.domain.example.com",
		}
		
		for _, url := range specialURLs {
			if !IsValidURL(url) {
				t.Errorf("Expected %s to be valid", url)
			}
			
			domain, err := ExtractDomain(url)
			if err != nil {
				t.Errorf("Unexpected error extracting domain from %s: %v", url, err)
			}
			if domain == "" {
				t.Errorf("Expected non-empty domain for %s", url)
			}
		}
	})

	t.Run("ErrorHandlingEdgeCases", func(t *testing.T) {
		// Test SpiderError with empty fields
		err := NewSpiderError("", "", "")
		if err.Error() != ":  (URL: )" {
			t.Errorf("Unexpected error string for empty SpiderError: %s", err.Error())
		}
		
		// Test SpiderError with special characters
		err = NewSpiderError("TestError", "Error with special chars: !@#$%", "https://example.com")
		errorString := err.Error()
		if errorString == "" {
			t.Error("Expected non-empty error string")
		}
	})
}

// Test concurrent operations
func TestConcurrentOperations(t *testing.T) {
	t.Run("ConcurrentSpiderCreation", func(t *testing.T) {
		const numGoroutines = 10
		done := make(chan bool, numGoroutines)
		
		for i := 0; i < numGoroutines; i++ {
			go func() {
				config := NewSpiderConfig()
				spider, err := NewSpider(config)
				if err != nil {
					t.Errorf("Unexpected error in goroutine: %v", err)
				}
				if spider != nil {
					spider.Close()
				}
				done <- true
			}()
		}
		
		for i := 0; i < numGoroutines; i++ {
			<-done
		}
	})

	t.Run("ConcurrentURLProcessing", func(t *testing.T) {
		const numGoroutines = 10
		urls := []string{
			"https://example.com",
			"https://google.com",
			"https://github.com",
		}
		done := make(chan bool, numGoroutines)
		
		for i := 0; i < numGoroutines; i++ {
			go func() {
				for _, url := range urls {
					_, err := ProcessURL(url)
					if err != nil {
						t.Errorf("Unexpected error processing %s: %v", url, err)
					}
				}
				done <- true
			}()
		}
		
		for i := 0; i < numGoroutines; i++ {
			<-done
		}
	})
}
