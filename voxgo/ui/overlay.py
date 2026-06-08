"""Backward-compatible overlay UI exports."""

from voxgo.ui.config_models import (  # noqa: F401
    AudioDeviceConfig,
    DebugConfig,
    HotkeyConfig,
    OverlayConfig,
    RuntimeConfig,
    WhisperDeviceConfig,
)
from voxgo.ui.dialogs import (  # noqa: F401
    FeedbackDialog,
    FirstRunWizard,
    FullscreenHelpDialog,
    UpdatePromptDialog,
)
from voxgo.ui.overlay_window import GameOverlay, OverlaySignals, TranslationItem  # noqa: F401
from voxgo.ui.settings_dialog import SettingsDialog  # noqa: F401
from voxgo.ui.widgets import (  # noqa: F401
    AudioTestPanel,
    AudioTestSignals,
    ColorButton,
    HotkeyCaptureEdit,
    OverlayLockButton,
    TranslationTestRunner,
    TranslationTestSignals,
)
