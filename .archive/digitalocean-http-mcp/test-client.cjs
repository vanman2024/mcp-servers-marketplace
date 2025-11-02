#!/usr/bin/env node
/**
 * Node.js test client for Digital Ocean MCP Server
 * Handles SSE (Server-Sent Events) properly
 */

const https = require('https');
const http = require('http');

class MCPClient {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
        this.sessionId = null;
    }

    async makeRequest(method, params) {
        return new Promise((resolve, reject) => {
            const url = new URL(this.baseUrl);
            const postData = JSON.stringify({
                jsonrpc: '2.0',
                method: method,
                params: params,
                id: Date.now()
            });

            const options = {
                hostname: url.hostname,
                port: url.port,
                path: url.pathname,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'text/event-stream',
                    'Content-Length': Buffer.byteLength(postData)
                }
            };

            const req = http.request(options, (res) => {
                let data = '';

                res.on('data', (chunk) => {
                    data += chunk;
                    
                    // Parse SSE data
                    const lines = data.split('\n');
                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            try {
                                const json = JSON.parse(line.slice(6));
                                if (json.result || json.error) {
                                    resolve(json);
                                    return;
                                }
                            } catch (e) {
                                // Continue collecting data
                            }
                        }
                    }
                });

                res.on('end', () => {
                    reject(new Error('Connection closed without complete response'));
                });
            });

            req.on('error', reject);
            req.write(postData);
            req.end();
        });
    }

    async initialize() {
        console.log('🔌 Initializing connection...');
        const result = await this.makeRequest('initialize', {
            protocolVersion: '0.1.0',
            capabilities: {},
            clientInfo: {
                name: 'DO MCP Test Client',
                version: '1.0.0'
            }
        });
        
        if (result.result) {
            console.log(`✅ Connected to: ${result.result.serverInfo.name}`);
            return true;
        }
        return false;
    }

    async callTool(toolName, args = {}) {
        console.log(`\n🔧 Calling tool: ${toolName}`);
        const result = await this.makeRequest('tools/call', {
            name: toolName,
            arguments: args
        });
        
        if (result.error) {
            console.error(`❌ Error: ${result.error.message}`);
            return null;
        }
        
        return result.result;
    }

    async getResource(uri) {
        console.log(`\n📚 Getting resource: ${uri}`);
        const result = await this.makeRequest('resources/read', {
            uri: `resource://${uri}`
        });
        
        if (result.error) {
            console.error(`❌ Error: ${result.error.message}`);
            return null;
        }
        
        return result.result;
    }

    async getPrompt(name, args = {}) {
        console.log(`\n💡 Getting prompt: ${name}`);
        const result = await this.makeRequest('prompts/get', {
            name: name,
            arguments: args
        });
        
        if (result.error) {
            console.error(`❌ Error: ${result.error.message}`);
            return null;
        }
        
        return result.result;
    }
}

async function runTests() {
    const client = new MCPClient('http://localhost:8040/');
    
    try {
        // Initialize
        if (!await client.initialize()) {
            console.error('Failed to initialize');
            return;
        }

        // Test 1: Get Account Info
        const account = await client.callTool('get_account_info');
        if (account) {
            console.log('Account Info:', JSON.stringify(account, null, 2));
        }

        // Test 2: List Droplets
        const droplets = await client.callTool('list_droplets');
        if (droplets) {
            console.log(`\nFound ${droplets.total} droplets`);
            droplets.droplets.forEach(d => {
                console.log(`  - ${d.name} (${d.status}) - ${d.ip_address}`);
            });
        }

        // Test 3: List SSH Keys
        const keys = await client.callTool('list_ssh_keys');
        if (keys) {
            console.log(`\nFound ${keys.total} SSH keys`);
            keys.ssh_keys.forEach(k => {
                console.log(`  - ${k.name}: ${k.fingerprint}`);
            });
        }

        // Test 4: Create Droplet (mock)
        const newDroplet = await client.callTool('create_droplet', {
            name: 'test-node-client',
            region: 'nyc3',
            size: 's-1vcpu-1gb',
            image: 'ubuntu-22-04-x64',
            tags: ['test', 'mcp']
        });
        if (newDroplet) {
            console.log('\nCreated droplet:', newDroplet.droplet.name);
        }

        // Test 5: List Databases
        const databases = await client.callTool('list_databases');
        if (databases) {
            console.log(`\nFound ${databases.total} databases`);
        }

        // Test 6: Get Resource - Regions
        const regions = await client.getResource('regions');
        if (regions) {
            const regionData = JSON.parse(regions.contents[0].text);
            console.log('\nAvailable regions:', Object.keys(regionData.regions).join(', '));
        }

        // Test 7: Get Prompt
        const prompt = await client.getPrompt('droplet_creation_guide', {
            purpose: 'web_server',
            environment: 'production'
        });
        if (prompt) {
            console.log('\nPrompt preview:', prompt.messages[0].content.text.substring(0, 100) + '...');
        }

        console.log('\n✅ All tests completed!');

    } catch (error) {
        console.error('Test error:', error);
    }
}

// Run tests
console.log('🌊 Digital Ocean MCP Server Test Client');
console.log('=' .repeat(50));
runTests();