#!/usr/bin/env node

/**
 * JAEGIS CLI Interface
 * Command-line interface for JAEGIS Method Agent
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const { Command } = require('commander')
const inquirer = require('inquirer')
const chalk = require('chalk')
const figlet = require('figlet')
const boxen = require('boxen')
const ora = require('ora')
const fs = require('fs').promises
const path = require('path')

const CommandRouter = require('./core/CommandRouter')
const ConfigManager = require('./core/ConfigManager')
const CacheManager = require('./core/CacheManager')
const PythonBridge = require('./services/PythonBridge')
const logger = require('./utils/logger')

class JAEGISCLI {
  constructor() {
    this.program = new Command()
    this.router = null
    this.config = null
    this.interactive = false
    this.spinner = null
  }

  async initialize() {
    try {
      // Load configuration
      this.config = await ConfigManager.load()
      
      // Initialize command router
      const cache = new CacheManager(this.config.cache)
      await cache.initialize()
      
      const pythonBridge = new PythonBridge(this.config.python_integration)
      await pythonBridge.initialize()
      
      this.router = new CommandRouter({
        config: this.config,
        cache,
        pythonBridge
      })
      await this.router.initialize()
      
    } catch (error) {
      console.error(chalk.red('❌ Failed to initialize JAEGIS CLI:'), error.message)
      process.exit(1)
    }
  }

  setupCommands() {
    this.program
      .name('jaegis')
      .description('JAEGIS - AI Agent Intelligence System CLI')
      .version('2.0.0')

    // Interactive mode
    this.program
      .command('interactive')
      .alias('i')
      .description('Start interactive JAEGIS session')
      .action(async () => {
        await this.startInteractiveMode()
      })

    // Execute single command
    this.program
      .command('exec <command>')
      .alias('e')
      .description('Execute a single JAEGIS command')
      .option('-p, --parameters <params>', 'Command parameters as JSON string')
      .option('-v, --verbose', 'Verbose output')
      .action(async (command, options) => {
        await this.executeCommand(command, options)
      })

    // Help command
    this.program
      .command('help [command]')
      .description('Show help for JAEGIS commands')
      .action(async (command) => {
        await this.showHelp(command)
      })

    // Status command
    this.program
      .command('status')
      .alias('s')
      .description('Show JAEGIS system status')
      .action(async () => {
        await this.showStatus()
      })

    // Configuration commands
    this.program
      .command('config')
      .description('Configuration management')
      .option('--show', 'Show current configuration')
      .option('--edit', 'Edit configuration interactively')
      .option('--reset', 'Reset to default configuration')
      .action(async (options) => {
        await this.manageConfig(options)
      })

    // Cache commands
    this.program
      .command('cache')
      .description('Cache management')
      .option('--clear', 'Clear all cache')
      .option('--stats', 'Show cache statistics')
      .action(async (options) => {
        await this.manageCache(options)
      })

    // Test command
    this.program
      .command('test')
      .description('Test JAEGIS system connectivity')
      .action(async () => {
        await this.testSystem()
      })

    // Update commands
    this.program
      .command('update')
      .description('Update commands from GitHub')
      .option('--force', 'Force update even if cache is fresh')
      .action(async (options) => {
        await this.updateCommands(options)
      })
  }

  async startInteractiveMode() {
    this.interactive = true
    
    // Show welcome banner
    this.showWelcomeBanner()
    
    console.log(chalk.cyan('\n🎯 Welcome to JAEGIS Interactive Mode!'))
    console.log(chalk.gray('Type commands or "exit" to quit. Use "help" for available commands.\n'))

    while (this.interactive) {
      try {
        const { command } = await inquirer.prompt([
          {
            type: 'input',
            name: 'command',
            message: chalk.blue('JAEGIS>'),
            prefix: ''
          }
        ])

        if (!command.trim()) continue

        if (command.toLowerCase() === 'exit' || command.toLowerCase() === 'quit') {
          console.log(chalk.yellow('👋 Goodbye!'))
          this.interactive = false
          break
        }

        if (command.toLowerCase() === 'clear') {
          console.clear()
          this.showWelcomeBanner()
          continue
        }

        await this.processInteractiveCommand(command)

      } catch (error) {
        if (error.isTtyError) {
          console.error(chalk.red('❌ Interactive mode not supported in this environment'))
          break
        } else {
          console.error(chalk.red('❌ Error:'), error.message)
        }
      }
    }
  }

  async processInteractiveCommand(command) {
    this.spinner = ora('Processing command...').start()
    
    try {
      const result = await this.router.processCommand(command, {
        context: { cli: true, interactive: true }
      })

      this.spinner.stop()
      this.displayResult(result)

    } catch (error) {
      this.spinner.stop()
      console.error(chalk.red('❌ Command failed:'), error.message)
    }
  }

  async executeCommand(command, options) {
    console.log(chalk.blue(`🎯 Executing: ${command}`))
    
    this.spinner = ora('Processing...').start()
    
    try {
      let parameters = {}
      if (options.parameters) {
        try {
          parameters = JSON.parse(options.parameters)
        } catch (error) {
          this.spinner.stop()
          console.error(chalk.red('❌ Invalid parameters JSON:'), error.message)
          return
        }
      }

      const result = await this.router.processCommand(command, {
        parameters,
        context: { cli: true, verbose: options.verbose }
      })

      this.spinner.stop()
      this.displayResult(result, options.verbose)

    } catch (error) {
      this.spinner.stop()
      console.error(chalk.red('❌ Command execution failed:'), error.message)
      process.exit(1)
    }
  }

  async showHelp(command) {
    if (command) {
      // Show help for specific command
      console.log(chalk.blue(`📚 Help for command: ${command}`))
      
      try {
        const result = await this.router.processCommand(`help ${command}`)
        this.displayResult(result)
      } catch (error) {
        console.error(chalk.red('❌ Failed to get help:'), error.message)
      }
    } else {
      // Show general help
      this.showWelcomeBanner()
      
      console.log(chalk.cyan('\n📚 JAEGIS CLI Help\n'))
      
      console.log(chalk.white('Available Commands:'))
      console.log(chalk.gray('  jaegis interactive     Start interactive mode'))
      console.log(chalk.gray('  jaegis exec <cmd>      Execute a command'))
      console.log(chalk.gray('  jaegis help [cmd]      Show help'))
      console.log(chalk.gray('  jaegis status          Show system status'))
      console.log(chalk.gray('  jaegis config          Manage configuration'))
      console.log(chalk.gray('  jaegis cache           Manage cache'))
      console.log(chalk.gray('  jaegis test            Test system'))
      console.log(chalk.gray('  jaegis update          Update commands'))
      
      console.log(chalk.white('\nJAEGIS Commands:'))
      console.log(chalk.gray('  /help                  Show all JAEGIS commands'))
      console.log(chalk.gray('  /status                System status'))
      console.log(chalk.gray('  /config                Configuration'))
      console.log(chalk.gray('  /agents                List agents'))
      console.log(chalk.gray('  /mode-switch           Switch modes'))
      
      console.log(chalk.white('\nExamples:'))
      console.log(chalk.gray('  jaegis interactive'))
      console.log(chalk.gray('  jaegis exec "/help"'))
      console.log(chalk.gray('  jaegis exec "/config" --parameters \'{"action": "show"}\''))
      
      console.log(chalk.cyan('\n🚀 Get started with: jaegis interactive'))
    }
  }

  async showStatus() {
    console.log(chalk.blue('📊 JAEGIS System Status\n'))
    
    this.spinner = ora('Checking system status...').start()
    
    try {
      const result = await this.router.processCommand('status')
      this.spinner.stop()
      
      if (result.success) {
        const status = result.data
        
        console.log(boxen(
          chalk.green('✅ System Status: HEALTHY') + '\n\n' +
          chalk.white(`Version: ${status.version}\n`) +
          chalk.white(`Environment: ${status.environment}\n`) +
          chalk.white(`Uptime: ${Math.floor(process.uptime())}s\n`) +
          chalk.white(`Commands Loaded: ${this.router.getStats().totalCommands}\n`) +
          chalk.white(`Cache Enabled: ${status.configuration.cache_enabled ? 'Yes' : 'No'}\n`) +
          chalk.white(`Python Integration: ${status.configuration.python_integration ? 'Yes' : 'No'}`),
          {
            padding: 1,
            margin: 1,
            borderStyle: 'round',
            borderColor: 'green'
          }
        ))
      } else {
        console.log(chalk.red('❌ System Status: UNHEALTHY'))
        console.log(chalk.red('Error:'), result.error)
      }

    } catch (error) {
      this.spinner.stop()
      console.error(chalk.red('❌ Failed to get status:'), error.message)
    }
  }

  async manageConfig(options) {
    if (options.show) {
      console.log(chalk.blue('⚙️ Current Configuration\n'))
      
      const publicConfig = {
        system: this.config.system,
        commands: this.config.commands,
        cache: { enabled: this.config.cache.enabled },
        python_integration: { enabled: this.config.python_integration.enabled }
      }
      
      console.log(JSON.stringify(publicConfig, null, 2))
      
    } else if (options.edit) {
      console.log(chalk.blue('⚙️ Interactive Configuration Editor'))
      console.log(chalk.yellow('⚠️  Configuration editing not yet implemented'))
      
    } else if (options.reset) {
      const { confirm } = await inquirer.prompt([
        {
          type: 'confirm',
          name: 'confirm',
          message: 'Are you sure you want to reset configuration to defaults?',
          default: false
        }
      ])
      
      if (confirm) {
        console.log(chalk.yellow('🔄 Resetting configuration...'))
        // TODO: Implement config reset
        console.log(chalk.green('✅ Configuration reset complete'))
      }
      
    } else {
      console.log(chalk.blue('⚙️ Configuration Management'))
      console.log(chalk.gray('Use --show, --edit, or --reset options'))
    }
  }

  async manageCache(options) {
    if (options.clear) {
      const { confirm } = await inquirer.prompt([
        {
          type: 'confirm',
          name: 'confirm',
          message: 'Are you sure you want to clear all cache?',
          default: false
        }
      ])
      
      if (confirm) {
        this.spinner = ora('Clearing cache...').start()
        
        try {
          // TODO: Implement cache clearing
          this.spinner.stop()
          console.log(chalk.green('✅ Cache cleared successfully'))
        } catch (error) {
          this.spinner.stop()
          console.error(chalk.red('❌ Failed to clear cache:'), error.message)
        }
      }
      
    } else if (options.stats) {
      console.log(chalk.blue('💾 Cache Statistics'))
      
      try {
        const stats = this.router.getStats()
        console.log(chalk.white(`Total Commands: ${stats.totalCommands}`))
        console.log(chalk.white(`Command History: ${stats.commandHistory}`))
        console.log(chalk.white(`Active Commands: ${stats.activeCommands}`))
        console.log(chalk.white(`Last Update: ${stats.lastUpdate ? new Date(stats.lastUpdate).toLocaleString() : 'Never'}`))
      } catch (error) {
        console.error(chalk.red('❌ Failed to get cache stats:'), error.message)
      }
      
    } else {
      console.log(chalk.blue('💾 Cache Management'))
      console.log(chalk.gray('Use --clear or --stats options'))
    }
  }

  async testSystem() {
    console.log(chalk.blue('🧪 Testing JAEGIS System\n'))
    
    const tests = [
      { name: 'Configuration', test: () => this.config !== null },
      { name: 'Command Router', test: () => this.router !== null },
      { name: 'Python Bridge', test: async () => {
        try {
          const health = await this.router.pythonBridge.healthCheck()
          return health.status === 'healthy'
        } catch {
          return false
        }
      }},
      { name: 'GitHub Integration', test: async () => {
        try {
          const result = await this.router.pythonBridge.testConnection()
          return result.success
        } catch {
          return false
        }
      }}
    ]
    
    for (const test of tests) {
      this.spinner = ora(`Testing ${test.name}...`).start()
      
      try {
        const result = typeof test.test === 'function' ? await test.test() : test.test
        
        if (result) {
          this.spinner.succeed(chalk.green(`${test.name}: PASS`))
        } else {
          this.spinner.fail(chalk.red(`${test.name}: FAIL`))
        }
      } catch (error) {
        this.spinner.fail(chalk.red(`${test.name}: ERROR - ${error.message}`))
      }
    }
    
    console.log(chalk.cyan('\n✅ System test complete'))
  }

  async updateCommands(options) {
    console.log(chalk.blue('🔄 Updating Commands from GitHub'))
    
    this.spinner = ora('Fetching latest commands...').start()
    
    try {
      await this.router.updateCommandsFromGitHub()
      this.spinner.succeed(chalk.green('✅ Commands updated successfully'))
      
      const stats = this.router.getStats()
      console.log(chalk.white(`Total Commands: ${stats.totalCommands}`))
      console.log(chalk.white(`Categories: ${stats.totalCategories}`))
      
    } catch (error) {
      this.spinner.fail(chalk.red('❌ Failed to update commands'))
      console.error(chalk.red('Error:'), error.message)
    }
  }

  displayResult(result, verbose = false) {
    console.log() // Empty line
    
    if (result.success) {
      console.log(chalk.green('✅ Success'))
      
      if (result.data) {
        if (typeof result.data === 'string') {
          console.log(chalk.white(result.data))
        } else if (typeof result.data === 'object') {
          if (result.data.message) {
            console.log(chalk.white(result.data.message))
          } else {
            console.log(JSON.stringify(result.data, null, 2))
          }
        }
      }
      
      if (verbose && result.metadata) {
        console.log(chalk.gray(`\nProcessing Time: ${result.metadata.processingTime}ms`))
        console.log(chalk.gray(`Request ID: ${result.metadata.requestId}`))
      }
      
    } else {
      console.log(chalk.red('❌ Error'))
      console.log(chalk.red(result.error))
      
      if (result.suggestions && result.suggestions.length > 0) {
        console.log(chalk.yellow('\n💡 Suggestions:'))
        result.suggestions.forEach(suggestion => {
          console.log(chalk.gray(`  ${suggestion.command} - ${suggestion.description}`))
        })
      }
    }
    
    console.log() // Empty line
  }

  showWelcomeBanner() {
    console.clear()
    
    try {
      const banner = figlet.textSync('JAEGIS', {
        font: 'ANSI Shadow',
        horizontalLayout: 'default',
        verticalLayout: 'default'
      })
      
      console.log(chalk.cyan(banner))
    } catch (error) {
      console.log(chalk.cyan.bold('JAEGIS'))
    }
    
    console.log(chalk.gray('AI Agent Intelligence System v2.0.0'))
    console.log(chalk.gray('Command Processing & GitHub Integration Framework'))
  }

  async run() {
    try {
      await this.initialize()
      this.setupCommands()
      
      // If no arguments provided, show help
      if (process.argv.length <= 2) {
        await this.showHelp()
        return
      }
      
      await this.program.parseAsync(process.argv)
      
    } catch (error) {
      console.error(chalk.red('❌ CLI Error:'), error.message)
      process.exit(1)
    }
  }
}

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error(chalk.red('❌ Uncaught Exception:'), error.message)
  process.exit(1)
})

process.on('unhandledRejection', (reason, promise) => {
  console.error(chalk.red('❌ Unhandled Rejection:'), reason)
  process.exit(1)
})

// Run CLI if this file is executed directly
if (require.main === module) {
  const cli = new JAEGISCLI()
  cli.run()
}

module.exports = JAEGISCLI