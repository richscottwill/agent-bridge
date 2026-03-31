# Requirements Document

## Introduction

The AgentSpaces Desktop Launcher is a desktop application that streamlines the workflow of spinning up a new AgentSpace and connecting to it from the Kiro desktop IDE via SSH. Currently, launching an AgentSpace and connecting to it requires multiple manual steps across different interfaces — navigating to the AgentSpaces web console, creating a new space, waiting for provisioning, configuring SSH, and opening Kiro. This tool collapses that workflow into a single launch action: authenticate, create the AgentSpace, wait for it to become ready, configure the SSH tunnel, and open Kiro connected to the remote environment.

## Glossary

- **Launcher**: The desktop application that orchestrates AgentSpace creation, SSH configuration, and Kiro launch
- **AgentSpace**: An Amazon AI-powered containerized development environment provisioned through the AgentSpaces service
- **AgentSpaces_API**: The backend API that the Launcher calls to create, query, and manage AgentSpaces
- **SSH_Configurator**: The component responsible for generating and managing SSH configuration entries for connecting to AgentSpaces
- **Kiro_Desktop**: The Kiro desktop IDE application installed on the user's local machine
- **Space_Provisioner**: The component that handles the creation request and monitors provisioning status of a new AgentSpace
- **Auth_Manager**: The component responsible for authenticating the user against Amazon's identity systems before making API calls
- **Connection_Monitor**: The component that verifies SSH connectivity to the provisioned AgentSpace before launching Kiro
- **Space_Profile**: A saved configuration specifying AgentSpace parameters (instance type, timeout, attached repositories) for quick re-launch
- **Provisioning_State**: The lifecycle state of an AgentSpace: REQUESTED, PROVISIONING, RUNNING, STOPPING, STOPPED, FAILED

## Requirements

### Requirement 1: User Authentication

**User Story:** As a developer, I want the Launcher to authenticate me against Amazon's identity systems, so that I can securely create and connect to AgentSpaces without managing credentials manually.

#### Acceptance Criteria

1. WHEN the Launcher starts, THE Auth_Manager SHALL check for an existing valid authentication session
2. WHEN no valid session exists, THE Auth_Manager SHALL initiate the Amazon SSO authentication flow
3. WHEN authentication succeeds, THE Auth_Manager SHALL store the session token for reuse across subsequent operations within the same Launcher session
4. IF authentication fails, THEN THE Auth_Manager SHALL display a descriptive error message indicating the failure reason and offer a retry option
5. WHEN the session token expires during an active Launcher session, THE Auth_Manager SHALL re-authenticate transparently without losing the current operation state

### Requirement 2: AgentSpace Creation

**User Story:** As a developer, I want to launch a new AgentSpace with a single action, so that I do not have to navigate the web console and fill out forms manually each time.

#### Acceptance Criteria

1. WHEN the user triggers a launch, THE Space_Provisioner SHALL send a creation request to the AgentSpaces_API with the configured parameters
2. WHEN creating an AgentSpace, THE Space_Provisioner SHALL allow the user to specify instance type, idle timeout, and repository attachments
3. WHEN the AgentSpaces_API accepts the creation request, THE Space_Provisioner SHALL transition the Provisioning_State to REQUESTED
4. IF the AgentSpaces_API rejects the creation request, THEN THE Space_Provisioner SHALL display the rejection reason to the user
5. WHEN the user has a saved Space_Profile, THE Launcher SHALL pre-populate creation parameters from the selected profile
6. THE Launcher SHALL allow the user to save current creation parameters as a new Space_Profile for future use

### Requirement 3: Provisioning Status Monitoring

**User Story:** As a developer, I want to see real-time provisioning progress, so that I know when my AgentSpace is ready and can diagnose delays or failures.

#### Acceptance Criteria

1. WHILE the Provisioning_State is REQUESTED or PROVISIONING, THE Space_Provisioner SHALL poll the AgentSpaces_API for status updates at a regular interval
2. WHEN the Provisioning_State transitions, THE Launcher SHALL display the current state and elapsed time to the user
3. WHEN the Provisioning_State reaches RUNNING, THE Space_Provisioner SHALL proceed to SSH configuration
4. IF the Provisioning_State reaches FAILED, THEN THE Space_Provisioner SHALL display the failure reason and offer options to retry or cancel
5. WHEN provisioning exceeds a configurable timeout threshold, THE Launcher SHALL warn the user that provisioning is taking longer than expected and offer the option to cancel

### Requirement 4: SSH Configuration

**User Story:** As a developer, I want the Launcher to automatically configure SSH for the new AgentSpace, so that I do not have to manually edit SSH config files or look up connection details.

#### Acceptance Criteria

1. WHEN the AgentSpace reaches RUNNING state, THE SSH_Configurator SHALL retrieve the SSH connection details from the AgentSpaces_API
2. WHEN configuring SSH, THE SSH_Configurator SHALL add or update an SSH config entry for the AgentSpace in the user's SSH configuration file
3. WHEN writing SSH configuration, THE SSH_Configurator SHALL preserve all existing entries in the SSH configuration file that are unrelated to AgentSpaces
4. WHEN configuring SSH, THE SSH_Configurator SHALL set the hostname, port, user, and identity file based on the AgentSpace connection details
5. IF the SSH configuration file does not exist, THEN THE SSH_Configurator SHALL create the file with appropriate permissions (600)
6. WHEN an SSH config entry for a previous AgentSpace with the same name exists, THE SSH_Configurator SHALL replace the old entry with the new connection details

### Requirement 5: SSH Connection Verification

**User Story:** As a developer, I want the Launcher to verify that the SSH connection works before opening Kiro, so that I am not left with a broken IDE session.

#### Acceptance Criteria

1. WHEN SSH configuration is complete, THE Connection_Monitor SHALL attempt an SSH connection to the AgentSpace
2. WHEN the SSH connection succeeds, THE Connection_Monitor SHALL proceed to launch Kiro_Desktop
3. IF the SSH connection fails, THEN THE Connection_Monitor SHALL retry the connection up to a configurable number of attempts with exponential backoff
4. IF all SSH connection retries are exhausted, THEN THE Connection_Monitor SHALL display the connection error and offer options to retry manually, reconfigure, or cancel
5. WHEN verifying the SSH connection, THE Connection_Monitor SHALL complete the verification within a configurable timeout period

### Requirement 6: Kiro Desktop Launch

**User Story:** As a developer, I want the Launcher to open Kiro Desktop connected to my new AgentSpace automatically, so that I go from zero to coding in one step.

#### Acceptance Criteria

1. WHEN the SSH connection is verified, THE Launcher SHALL launch Kiro_Desktop with the SSH remote connection target set to the new AgentSpace
2. IF Kiro_Desktop is not installed at the expected path, THEN THE Launcher SHALL display an error message indicating that Kiro Desktop is not found and provide installation guidance
3. WHEN launching Kiro_Desktop, THE Launcher SHALL pass the workspace directory path if one was specified in the Space_Profile or creation parameters
4. WHEN Kiro_Desktop launches successfully, THE Launcher SHALL minimize to the system tray or close based on user preference

### Requirement 7: Space Profile Management

**User Story:** As a developer, I want to save and reuse AgentSpace configurations, so that I can quickly launch spaces with my preferred settings without reconfiguring each time.

#### Acceptance Criteria

1. THE Launcher SHALL persist Space_Profiles to local storage so they survive application restarts
2. WHEN displaying saved profiles, THE Launcher SHALL show the profile name, instance type, and attached repositories
3. WHEN the user selects a saved Space_Profile, THE Launcher SHALL pre-populate all creation parameters from that profile
4. THE Launcher SHALL allow the user to edit and delete existing Space_Profiles
5. WHEN the user has exactly one Space_Profile saved, THE Launcher SHALL default to that profile on startup

### Requirement 8: Error Handling and Recovery

**User Story:** As a developer, I want clear error messages and recovery options at every stage, so that I can resolve issues without restarting the entire workflow from scratch.

#### Acceptance Criteria

1. IF an error occurs at any stage (authentication, creation, provisioning, SSH, launch), THEN THE Launcher SHALL display a human-readable error message with the failed stage identified
2. WHEN an error occurs after the AgentSpace has been successfully provisioned, THE Launcher SHALL offer to retry from the SSH configuration step without re-provisioning
3. WHEN an error occurs during provisioning, THE Launcher SHALL offer to retry the creation or cancel and clean up the failed request
4. THE Launcher SHALL log all operations and errors to a local log file for troubleshooting
5. IF the Launcher loses network connectivity during any operation, THEN THE Launcher SHALL detect the loss and pause the workflow until connectivity is restored

### Requirement 9: AgentSpace Lifecycle Visibility

**User Story:** As a developer, I want to see my existing AgentSpaces and their status, so that I can reconnect to a running space instead of always creating a new one.

#### Acceptance Criteria

1. WHEN the Launcher starts, THE Launcher SHALL fetch and display a list of the user's existing AgentSpaces with their current Provisioning_State
2. WHEN an existing AgentSpace is in RUNNING state, THE Launcher SHALL offer a "Connect" action that skips creation and proceeds directly to SSH configuration and Kiro launch
3. WHEN an existing AgentSpace is in STOPPED state, THE Launcher SHALL offer a "Start" action to resume the space before connecting
4. THE Launcher SHALL allow the user to stop or terminate AgentSpaces from the list view
5. WHEN displaying AgentSpaces, THE Launcher SHALL show the space name, instance type, creation time, and current state

### Requirement 10: Configuration Persistence

**User Story:** As a developer, I want my Launcher preferences (default instance type, timeout settings, Kiro path) persisted locally, so that the application remembers my settings across sessions.

#### Acceptance Criteria

1. THE Launcher SHALL persist user preferences to a local configuration file
2. WHEN the user modifies a preference, THE Launcher SHALL save the change immediately
3. THE Launcher SHALL provide a settings interface for configuring: default instance type, provisioning timeout, SSH retry count, SSH connection timeout, Kiro Desktop executable path, and post-launch behavior (minimize or close)
4. WHEN a required configuration value is missing, THE Launcher SHALL use a sensible default and inform the user

