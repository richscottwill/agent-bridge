# Implementation Plan: AgentSpaces Desktop Launcher

## Overview

Build an Electron + TypeScript desktop application that orchestrates AgentSpace creation, SSH configuration, and Kiro Desktop launch through a sequential pipeline. Implementation proceeds bottom-up: config store and data models first, then service layer components, then the orchestrator, and finally the Electron UI wiring.

## Tasks

- [x] 1. Initialize Electron project and core interfaces
  - [x] 1.1 Scaffold Electron + TypeScript project with build configuration
    - Initialize npm project with Electron, TypeScript, and required dev dependencies
    - Configure `tsconfig.json` for main (Node) and renderer processes
    - Set up basic Electron main process entry point and renderer HTML shell
    - _Requirements: All (project foundation)_

  - [x] 1.2 Define all TypeScript interfaces and types
    - Create `src/types.ts` with all interfaces from the design: `AuthSession`, `SpaceInfo`, `SpaceCreationParams`, `ProvisioningState`, `SSHConnectionDetails`, `SSHConfigEntry`, `SpaceProfile`, `UserPreferences`, `PipelineEvent`, `PipelineStage`, `PipelineState`, `PipelineError`, `LogEntry`, `RetryOptions`, `ConnectionResult`, `PollOptions`
    - _Requirements: All (shared type definitions)_

- [x] 2. Implement Config Store and Profile Manager
  - [x] 2.1 Implement ConfigStore with JSON file persistence
    - Create `src/services/config-store.ts` implementing the `ConfigStore` interface
    - Read/write a JSON file in the user's app data directory
    - Implement `get`, `set`, `delete` methods with type-safe access
    - Provide sensible defaults for `UserPreferences` when values are missing
    - _Requirements: 10.1, 10.2, 10.4_

  - [x] 2.2 Write unit tests for ConfigStore
    - Test get/set/delete operations
    - Test default value fallback when keys are missing
    - Test file creation when config file does not exist
    - _Requirements: 10.1, 10.4_

  - [x] 2.3 Implement ProfileManager with CRUD operations
    - Create `src/services/profile-manager.ts` implementing the `ProfileManager` interface
    - Store profiles in the ConfigStore under a `profiles` key
    - Implement `listProfiles`, `getProfile`, `saveProfile`, `deleteProfile`, `getDefaultProfile`
    - When exactly one profile exists, `getDefaultProfile` returns it
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

  - [x] 2.4 Write unit tests for ProfileManager
    - Test CRUD operations on profiles
    - Test default profile logic (single profile = default)
    - Test persistence across save/load cycles
    - _Requirements: 7.1, 7.4, 7.5_

- [x] 3. Implement Auth Manager
  - [x] 3.1 Implement AuthManager with SSO authentication flow
    - Create `src/services/auth-manager.ts` implementing the `AuthManager` interface
    - Implement `checkSession` to look for a cached valid session (check `expiresAt` against current time)
    - Implement `authenticate` to initiate Amazon SSO device authorization flow
    - Implement `refreshSession` to transparently re-authenticate when token expires
    - Store session in memory for reuse within the Launcher session
    - Return descriptive errors on authentication failure
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

  - [x] 3.2 Write unit tests for AuthManager
    - Test session validity check (valid, expired, missing)
    - Test error handling on authentication failure
    - Test transparent refresh behavior
    - _Requirements: 1.1, 1.4, 1.5_

- [x] 4. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implement Space Provisioner
  - [x] 5.1 Implement SpaceProvisioner with API integration
    - Create `src/services/space-provisioner.ts` implementing the `SpaceProvisioner` interface
    - Implement `createSpace` to send creation request to AgentSpaces API with configured parameters (instance type, idle timeout, repositories)
    - Implement `getSpaceStatus` to fetch current space state
    - Implement `listSpaces` to retrieve all spaces for the authenticated user
    - Implement `startSpace`, `stopSpace`, `terminateSpace` for lifecycle management
    - Implement `pollUntilReady` as an `AsyncGenerator` that yields `SpaceInfo` at configurable intervals until state reaches `RUNNING` or `FAILED`
    - Respect configurable timeout from `UserPreferences.provisioningTimeoutMs`
    - Surface API rejection reasons to the caller
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 3.5, 9.1, 9.3, 9.4_

  - [x] 5.2 Write unit tests for SpaceProvisioner
    - Test creation request parameter passing
    - Test polling loop transitions (REQUESTED → PROVISIONING → RUNNING)
    - Test polling timeout behavior
    - Test FAILED state handling
    - _Requirements: 2.1, 3.1, 3.4, 3.5_

- [ ] 6. Implement SSH Configurator
  - [x] 6.1 Implement SSHConfigurator with config file management
    - Create `src/services/ssh-configurator.ts` implementing the `SSHConfigurator` interface
    - Implement `configureSpace` to add/update an SSH config entry using `BEGIN`/`END` comment markers for the given space ID
    - Implement `removeSpace` to delete the marked block for a space
    - Implement `parseConfig` to read and parse the SSH config file into `SSHConfigEntry[]`
    - Preserve all non-AgentSpace entries when writing
    - Create the SSH config file with permissions 600 if it does not exist
    - Set hostname, port, user, identity file, and `StrictHostKeyChecking no` per the design format
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

  - [x] 6.2 Write unit tests for SSHConfigurator
    - Test adding a new entry to an empty config
    - Test updating an existing AgentSpace entry
    - Test preserving unrelated SSH entries
    - Test file creation with correct permissions
    - _Requirements: 4.2, 4.3, 4.5, 4.6_

- [ ] 7. Implement Connection Monitor
  - [x] 7.1 Implement ConnectionMonitor with retry and exponential backoff
    - Create `src/services/connection-monitor.ts` implementing the `ConnectionMonitor` interface
    - Implement `verifyConnection` to attempt SSH connection using the host alias
    - Implement exponential backoff retry logic with configurable `maxRetries`, `timeoutMs`, and `backoffBaseMs`
    - Return `ConnectionResult` with success status, attempt count, and error details
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [x] 7.2 Write unit tests for ConnectionMonitor
    - Test successful connection on first attempt
    - Test retry with exponential backoff timing
    - Test exhausted retries returning failure
    - _Requirements: 5.1, 5.3, 5.4_

- [ ] 8. Implement Kiro Launcher
  - [x] 8.1 Implement KiroLauncher for subprocess management
    - Create `src/services/kiro-launcher.ts` implementing the `KiroLauncher` interface
    - Implement `isInstalled` to check if Kiro Desktop exists at the configured path
    - Implement `getExecutablePath` to return the path from `UserPreferences.kiroExecutablePath`
    - Implement `launch` to spawn Kiro Desktop as a detached subprocess with the SSH remote target and optional workspace directory
    - Return descriptive error when Kiro is not found
    - _Requirements: 6.1, 6.2, 6.3_

  - [x] 8.2 Write unit tests for KiroLauncher
    - Test `isInstalled` with existing and missing executable
    - Test launch command construction with and without workspace directory
    - _Requirements: 6.1, 6.2, 6.3_

- [ ] 9. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 10. Implement Orchestrator and Logger
  - [x] 10.1 Implement logging utility
    - Create `src/services/logger.ts` that writes `LogEntry` records to a local log file
    - Support `info`, `warn`, `error` levels with stage tagging
    - _Requirements: 8.4_

  - [x] 10.2 Implement Orchestrator pipeline
    - Create `src/services/orchestrator.ts` implementing the `Orchestrator` interface
    - Implement `launch` as an `AsyncGenerator<PipelineEvent>` that executes stages sequentially: auth → create → provision (poll) → ssh_config → ssh_verify → kiro_launch
    - Implement `reconnect` that skips creation/provisioning and starts from ssh_config for an existing running space
    - Emit `PipelineEvent` at each stage transition (started, progress, completed, failed)
    - Track `PipelineState` throughout execution
    - On error after provisioning, offer retry from ssh_config step (don't re-provision)
    - On error during provisioning, offer retry creation or cancel
    - Detect network connectivity loss and pause workflow until restored
    - Log all operations and errors via the logger
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 9.2_

  - [x] 10.3 Write unit tests for Orchestrator
    - Test full pipeline happy path (all stages complete)
    - Test reconnect flow skipping creation
    - Test error recovery from SSH stage without re-provisioning
    - Test provisioning failure with retry/cancel options
    - _Requirements: 8.1, 8.2, 8.3_

- [ ] 11. Implement Electron UI
  - [x] 11.1 Build main window with launch and space list views
    - Create the Electron renderer with two primary views: launch form and existing spaces list
    - Launch form: instance type selector, idle timeout input, repository attachments, workspace directory, profile selector dropdown
    - Pre-populate form from selected `SpaceProfile` when one is chosen
    - Existing spaces list: show space name, instance type, creation time, current state
    - Show "Connect" action for RUNNING spaces, "Start" action for STOPPED spaces, "Stop"/"Terminate" actions for lifecycle management
    - _Requirements: 2.2, 2.5, 7.2, 7.3, 9.1, 9.2, 9.3, 9.4, 9.5_

  - [x] 11.2 Build provisioning progress view
    - Display current pipeline stage, status message, and elapsed time during launch
    - Show provisioning state transitions in real time as the orchestrator emits events
    - Display timeout warning when provisioning exceeds threshold
    - Offer cancel option during provisioning
    - _Requirements: 3.1, 3.2, 3.4, 3.5_

  - [x] 11.3 Build error display and recovery UI
    - Display human-readable error messages with the failed stage identified
    - Show retry/reconfigure/cancel options contextually based on which stage failed
    - For post-provisioning errors, show "Retry from SSH" option
    - For provisioning errors, show "Retry creation" and "Cancel" options
    - _Requirements: 1.4, 2.4, 3.4, 5.4, 6.2, 8.1, 8.2, 8.3_

  - [x] 11.4 Build settings and profile management UI
    - Settings panel for configuring: default instance type, provisioning timeout, SSH retry count, SSH connection timeout, Kiro executable path, post-launch behavior (minimize/close), poll interval
    - Save changes immediately via ConfigStore
    - Profile management: create, edit, delete profiles; display profile name, instance type, repositories
    - _Requirements: 2.6, 7.1, 7.2, 7.4, 10.1, 10.2, 10.3_

- [ ] 12. Wire UI to Orchestrator via IPC
  - [x] 12.1 Set up Electron IPC bridge between renderer and main process
    - Define IPC channels for: launch, reconnect, list-spaces, start-space, stop-space, terminate-space, save-profile, delete-profile, get-preferences, set-preference
    - Main process handlers invoke the appropriate service methods
    - Stream `PipelineEvent` from orchestrator to renderer via IPC for real-time progress updates
    - _Requirements: All (integration layer)_

  - [x] 12.2 Implement post-launch behavior
    - After Kiro launches successfully, minimize to system tray or close the launcher window based on `UserPreferences.postLaunchBehavior`
    - Set up system tray icon with context menu for quick actions
    - _Requirements: 6.4_

- [ ] 13. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- The design specifies TypeScript throughout — all implementations use TypeScript
- The orchestrator is the integration point; all services are built and testable independently before wiring
