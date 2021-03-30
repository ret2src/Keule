# Keule
Experimental, context-aware common password generator.


# Use Cases
- default credentials
- corporate password patterns 
- password reuse

# Classes

## Login
A username, e-mail or any other type of account

## Password
The actual password 

## Credential
A combindation of Login and Password

## Scope
Scope of an engagement, contains context information about the company and so on

## Context 
The context in which dictionaries are created (i.e. Scope, Inputs, Pipelines and output formats)

## CredentialPipeline
Selects Logins and Passwords from a given set, expands them based on a set of Rules and combines them to Credentials using CredentialMergers

## CredentialMerger
Combines a given set of Logins and Passwords to Credentials

