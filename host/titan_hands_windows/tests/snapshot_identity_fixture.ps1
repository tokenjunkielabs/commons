param([Parameter(Mandatory = $true)][string]$BackendPath)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)

# Parse the backend and load only pure identity/traversal functions. Never dot-source
# backend.ps1: its top level installs native input types and enters dispatch.
$tokens = $null
$parseErrors = $null
$backendAst = [System.Management.Automation.Language.Parser]::ParseFile(
    $BackendPath, [ref]$tokens, [ref]$parseErrors
)
if ($parseErrors.Count) { throw "backend parse errors: $($parseErrors -join '; ')" }
$required = @("Get-Field", "Try-Value", "Element-Identity", "Same-Element", "Queue-Children", "Snapshot", "Need-Element")
foreach ($name in $required) {
    $matching = @($backendAst.FindAll({
        param($entry)
        $entry -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $entry.Name -eq $name
    }, $false))
    if ($matching.Count -ne 1) { throw "expected exactly one backend function: $name" }
    . ([scriptblock]::Create($matching[0].Extent.Text))
}

function New-FakeElement([string]$Tag, [int[]]$RuntimeId = @(), [int]$Handle = 0, [string]$AutomationId = "same") {
    $element = [pscustomobject]@{
        Tag = $Tag
        RuntimeIds = $RuntimeId
        RuntimeReads = 0
        ThrowRuntimeId = $false
        Values = @{ ProcessId = 7; NativeWindowHandle = $Handle; AutomationId = $AutomationId }
        ReadCounts = @{ ProcessId = 0; NativeWindowHandle = 0; AutomationId = 0 }
        Children = @()
        Next = $null
        Current = $null
    }
    $element.Current = [pscustomobject]@{
        Owner = $element
        Name = "Identical control"
        IsOffscreen = $false
        HasKeyboardFocus = $false
    }
    $element.Current | Add-Member -MemberType ScriptProperty -Name ProcessId -Value {
        $this.Owner.ReadCounts.ProcessId += 1
        return $this.Owner.Values.ProcessId
    }
    $element.Current | Add-Member -MemberType ScriptProperty -Name NativeWindowHandle -Value {
        $this.Owner.ReadCounts.NativeWindowHandle += 1
        return $this.Owner.Values.NativeWindowHandle
    }
    $element.Current | Add-Member -MemberType ScriptProperty -Name AutomationId -Value {
        $this.Owner.ReadCounts.AutomationId += 1
        return $this.Owner.Values.AutomationId
    }
    $element | Add-Member -MemberType ScriptMethod -Name GetRuntimeId -Value {
        $this.RuntimeReads += 1
        if ($this.ThrowRuntimeId) { throw "runtime ID unavailable" }
        return $this.RuntimeIds
    }
    return $element
}

function Set-Children($Parent, [object[]]$Children) {
    $Parent.Children = @($Children)
    for ($index = 0; $index -lt $Children.Count; $index++) {
        $Children[$index].Next = if ($index + 1 -lt $Children.Count) { $Children[$index + 1] } else { $null }
    }
}

function New-FakeWalker {
    $walker = [pscustomobject]@{ FirstReads = @{}; SiblingReads = 0 }
    $walker | Add-Member -MemberType ScriptMethod -Name GetFirstChild -Value {
        param($element)
        if (-not $this.FirstReads.ContainsKey($element.Tag)) { $this.FirstReads[$element.Tag] = 0 }
        $this.FirstReads[$element.Tag] += 1
        if ($this.FirstReads[$element.Tag] -gt 100) { throw "fixture traversal guard" }
        if ($element.Children.Count) { return $element.Children[0] }
        return $null
    }
    $walker | Add-Member -MemberType ScriptMethod -Name GetNextSibling -Value {
        param($element)
        $this.SiblingReads += 1
        if ($this.SiblingReads -gt 100) { throw "fixture sibling guard" }
        return $element.Next
    }
    return $walker
}

# Serialization and UIA patterns are outside this fixture. Production Snapshot
# owns registration, so the fixture does not reconstruct or repair the action map.
function Element-Node($Element, [string]$ParentId, [string]$Id, $Identity) {
    if (-not $script:NodeCalls.ContainsKey($Element.Tag)) { $script:NodeCalls[$Element.Tag] = 0 }
    $script:NodeCalls[$Element.Tag] += 1
    return [ordered]@{
        id = $Id
        parent = $ParentId
        tag = $Element.Tag
        name = $Element.Current.Name
        states = @(if ($Element.Current.HasKeyboardFocus) { "focused" })
    }
}

function Observe-Fixture($Root, [object[]]$Elements, $Focused = $null, [bool]$IncludeOffscreen = $false, [int]$MaxNodes = 100) {
    $script:Walker = New-FakeWalker
    $script:NodeCalls = @{}
    if ($null -eq $Focused) { $Focused = New-FakeElement "outside_focus" }
    $request = [pscustomobject]@{ max_nodes = $MaxNodes; max_depth = 3; include_offscreen = $IncludeOffscreen }
    $snapshot = Snapshot $request $Root $Focused
    $lookups = @{}
    foreach ($node in $snapshot.nodes) {
        $resolved = Need-Element ([pscustomobject]@{ id = $node.id })
        $lookups[$node.id] = $resolved.Tag
    }
    $reads = @{}
    foreach ($element in $Elements) {
        $reads[$element.Tag] = @{
            process_id = $element.ReadCounts.ProcessId
            runtime_id = $element.RuntimeReads
            native_handle = $element.ReadCounts.NativeWindowHandle
            automation_id = $element.ReadCounts.AutomationId
        }
    }
    return [ordered]@{
        snapshot = $snapshot
        lookups = $lookups
        identity_reads = $reads
        node_calls = $script:NodeCalls
        first_child_calls = $script:Walker.FirstReads
        sibling_calls = $script:Walker.SiblingReads
    }
}

$cases = [ordered]@{}

$root = New-FakeElement "root"
$parentA = New-FakeElement "parent_a" @(101)
$parentB = New-FakeElement "parent_b" @(202)
$sharedA = New-FakeElement "shared_a" @(303)
$sharedB = New-FakeElement "shared_b" @(303) 0 "late-alias"
$leafA = New-FakeElement "leaf_a"
$leafB = New-FakeElement "leaf_b"
Set-Children $root @($parentA, $parentB)
Set-Children $parentA @($sharedA)
Set-Children $parentB @($sharedB)
Set-Children $sharedA @($leafA)
Set-Children $sharedB @($leafB)
$cases.strong_duplicate = Observe-Fixture $root @($parentA, $parentB, $sharedA, $sharedB, $leafA, $leafB)

$root = New-FakeElement "root"
$parent = New-FakeElement "parent" @(101)
$weakA = New-FakeElement "weak_a"
$weakB = New-FakeElement "weak_b"
Set-Children $root @($parent)
Set-Children $parent @($weakA, $weakB)
$cases.weak_siblings = Observe-Fixture $root @($parent, $weakA, $weakB)

$root = New-FakeElement "root"
$parentA = New-FakeElement "parent_a" @(101)
$parentB = New-FakeElement "parent_b" @(202)
$weakA = New-FakeElement "weak_a"
$weakB = New-FakeElement "weak_b"
Set-Children $root @($parentA, $parentB)
Set-Children $parentA @($weakA)
Set-Children $parentB @($weakB)
$cases.weak_parent_paths = Observe-Fixture $root @($parentA, $parentB, $weakA, $weakB)

$root = New-FakeElement "root"
$parent = New-FakeElement "parent" @(101)
$weakA = New-FakeElement "weak_a" @() 8128
$weakB = New-FakeElement "weak_b" @() 8128
Set-Children $root @($parent)
Set-Children $parent @($weakA, $weakB)
$cases.handle_only_collision = Observe-Fixture $root @($parent, $weakA, $weakB)

$root = New-FakeElement "root"
$parent = New-FakeElement "parent" @(101)
$offscreen = New-FakeElement "offscreen"
$visible = New-FakeElement "visible"
$offscreen.Current.IsOffscreen = $true
Set-Children $root @($parent)
Set-Children $parent @($offscreen, $visible)
$cases.filter_hidden = Observe-Fixture $root @($parent, $offscreen, $visible)
$cases.filter_included = Observe-Fixture $root @($parent, $offscreen, $visible) -IncludeOffscreen $true

$root = New-FakeElement "root"
$parent = New-FakeElement "parent" @(101)
$weakA = New-FakeElement "weak_a"
$weakB = New-FakeElement "weak_b"
Set-Children $root @($parent)
Set-Children $parent @($weakA, $weakB)
$cases.weak_focus_reference = Observe-Fixture $root @($parent, $weakA, $weakB) $weakB
$weakB.Current.HasKeyboardFocus = $true
$cases.weak_focus_state = Observe-Fixture $root @($parent, $weakA, $weakB)
$cases.omitted_focus = Observe-Fixture $root @($parent, $weakA, $weakB) $weakB -MaxNodes 2

$strong = New-FakeElement "strong_hash" @(42, 777) 456 "menu"
$cases.strong_hash = @{
    first = Element-Identity $strong "0.1"
    second = Element-Identity $strong "8.9"
}

$root = New-FakeElement "root"
$weak = New-FakeElement "weak"
$weak.ThrowRuntimeId = $true
Set-Children $root @($weak)
$cases.getter_once = Observe-Fixture $root @($weak)

$root = New-FakeElement "root"
$parent = New-FakeElement "parent" @(101)
$weakA = New-FakeElement "weak_a"
$weakB = New-FakeElement "weak_b"
Set-Children $root @($parent)
Set-Children $parent @($weakA, $weakB)
$weakB.Next = $weakA
$cases.sibling_cycle = Observe-Fixture $root @($parent, $weakA, $weakB)

$cases | ConvertTo-Json -Compress -Depth 14
