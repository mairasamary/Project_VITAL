<?php

declare(strict_types=1);

namespace OpenEMR\Tests\Isolated\ProjectVITAL;

use OpenEMR\Common\Logging\SystemLogger;
use PHPUnit\Framework\TestCase;

/**
 * Environment smoke test for Project VITAL.
 *
 * This test verifies that the OpenEMR autoloader and PHPUnit isolated-test
 * environment are working. It does not count as one of Assignment 3's
 * meaningful component unit tests.
 */
final class ProjectVITALSmokeTest extends TestCase
{
    public function testOpenEmrAutoloadingIsAvailable(): void
    {
        self::assertTrue(
            class_exists(SystemLogger::class),
            'OpenEMR Composer autoloading should resolve SystemLogger.'
        );
    }

    public function testPhpUnitRunsProjectVitalTests(): void
    {
        self::assertSame(4, 2 + 2);
    }
}
